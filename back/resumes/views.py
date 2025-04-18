
import os
from django.utils import timezone
from pydantic import ValidationError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg import openapi
from django.core.files.storage import default_storage
from .models import Resume, JobDescription, Log, MongoResume
from .serializers import ResumeSerializer, JobDescriptionSerializer
from .utils import process_resume, process_job_description, match_resume_to_job
from .permissions import IsRecruiter
from drf_yasg.utils import swagger_auto_schema
from bson import ObjectId
from django.core.cache import cache
from django.conf import settings
import json

class ResumeUploadView(generics.CreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Upload a resume for analysis",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='Resume file (PDF or DOCX)')
            },
            required=['file']
        ),
        responses={
            201: ResumeSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
            )
        }
    )
    def post(self, request, *args, **kwargs):
        existing_resume = MongoResume.objects.filter(user_id=self.request.user.id).first()
        if existing_resume:
            return Response(
                {'error': 'You already have a resume. Use the replace endpoint to update it.'},
                status=status.HTTP_403_FORBIDDEN
            )

        uploaded_file = self.request.FILES.get('file')
        if not uploaded_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file_path = default_storage.save(f'resumes/{uploaded_file.name}', uploaded_file)
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        file_url = f"{settings.MEDIA_URL}{file_path}"

        try:
            analysis = process_resume(full_file_path)
            print(f"Analysis result: {analysis}")

            mongo_resume = MongoResume(
                user_id=self.request.user.id,
                file=file_url,
                uploaded_at=timezone.now(),
                skills=analysis['skills'],
                experience=analysis['experience'],
                education=analysis['education'],
                rating=analysis['rating'],
                feedback=analysis['feedback']
            )
            mongo_resume.save()
            print(f"Saved MongoResume: {mongo_resume.id}, skills: {mongo_resume.skills}")

            Log.objects.using('mysql').create(
                user_id=self.request.user.id,
                action="Uploaded resume",
                details=f"Resume ID: {mongo_resume.id}"
            )

            serializer = self.serializer_class(mongo_resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            default_storage.delete(file_path)
            return Response({'error': f"AI validation failed: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            default_storage.delete(file_path)
            return Response({'error': f"Failed to process resume: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)
class ResumeDetailView(generics.RetrieveAPIView):
    queryset = Resume.objects.using('mongo').all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.using('mongo').filter(user=self.request.user)


class JobDescriptionCreateView(generics.CreateAPIView):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer
    permission_classes = [IsRecruiter]

    @swagger_auto_schema(
        operation_description="Create a job description and match it with resumes",
        request_body=JobDescriptionSerializer,
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'job': JobDescriptionSerializer,
                    'matches': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
            )
        }
    )
    def perform_create(self, serializer):
        job = serializer.save(recruiter=self.request.user)
        analysis = process_job_description(job.description)
        job.required_skills = ', '.join(analysis['required_skills'])
        job.required_experience = analysis['required_experience']
        job.save()
        cache.delete('job_description_list')
        print("Cache cleared after job creation")

        Log.objects.using('mysql').create(
            user_id=self.request.user.id,
            action="Created job description",
            details=f"Job ID: {job.id}"
        )

        resumes = MongoResume.objects.all()
        if not resumes:
            return Response({
                'job': JobDescriptionSerializer(job).data,
                'matches': [],
                'message': 'No resumes available for matching'
            })

        matches = []
        for resume in resumes:
            try:
                match = match_resume_to_job(resume, job)
                matches.append(match)
            except Exception as e:
                print(f"Error matching resume {resume.id}: {str(e)}")
                continue

        matches = sorted(matches, key=lambda x: x['compatibility_score'], reverse=True)
        return Response({
            'job': JobDescriptionSerializer(job).data,
            'matches': matches[:10]
        })


class JobDescriptionMatchView(generics.ListAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        try:
            job = JobDescription.objects.get(id=job_id, recruiter=self.request.user)
            resumes = MongoResume.objects.all()
            matches = [match_resume_to_job(resume, job) for resume in resumes]
            matches = sorted(matches, key=lambda x: x['compatibility_score'], reverse=True)
            matched_resume_ids = [ObjectId(match['resume_id']) for match in matches[:10]]
            return MongoResume.objects.filter(id__in=matched_resume_ids)
        except JobDescription.DoesNotExist:
            return MongoResume.objects.none()
        except ValueError as e:
            print(f"Invalid resume_id: {str(e)}")
            return MongoResume.objects.none()

    def list(self, request, *args, **kwargs):
        job_id = self.kwargs['job_id']
        try:
            job = JobDescription.objects.get(id=job_id, recruiter=self.request.user)
            queryset = self.get_queryset()
            matches = [match_resume_to_job(resume, job) for resume in queryset]
            return Response(matches)
        except JobDescription.DoesNotExist:
            return Response({'error': 'Job description not found or you are not authorized'},
                            status=status.HTTP_404_NOT_FOUND)


class JobDescriptionListView(generics.ListAPIView):
    serializer_class = JobDescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobDescription.objects.all()

    def list(self, request, *args, **kwargs):
        cache_key = 'job_description_list'

        cached_data = cache.get(cache_key)
        if cached_data:
            print("Returning data from cache")
            return Response(json.loads(cached_data))

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data

        cache.set(cache_key, json.dumps(data), timeout=60 * 15)
        print("Data cached")

        return Response(data)


class JobDescriptionDetailView(generics.RetrieveAPIView):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer
    permission_classes = [IsAuthenticated]

class ResumeReplaceView(generics.UpdateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Replace the existing resume with a new document",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='New resume file (PDF or DOCX)')
            },
            required=['file']
        ),
        responses={
            200: ResumeSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
            )
        }
    )
    def put(self, request, *args, **kwargs):
        existing_resume = MongoResume.objects.filter(user_id=self.request.user.id).first()
        if not existing_resume:
            return Response(
                {'error': 'No existing resume found. Please upload a resume first.'},
                status=status.HTTP_404_NOT_FOUND
            )

        uploaded_file = self.request.FILES.get('file')
        if not uploaded_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        old_file_path = existing_resume.file.replace(settings.MEDIA_URL, '')
        full_old_file_path = os.path.join(settings.MEDIA_ROOT, old_file_path)
        if os.path.exists(full_old_file_path):
            os.remove(full_old_file_path)

        new_file_path = default_storage.save(f'resumes/{uploaded_file.name}', uploaded_file)
        full_new_file_path = os.path.join(settings.MEDIA_ROOT, new_file_path)
        new_file_url = f"{settings.MEDIA_URL}{new_file_path}"

        try:
            analysis = process_resume(full_new_file_path)
            print(f"Analysis result: {analysis}")

            existing_resume.file = new_file_url
            existing_resume.uploaded_at = timezone.now()
            existing_resume.skills = analysis['skills']
            existing_resume.experience = analysis['experience']
            existing_resume.education = analysis['education']
            existing_resume.rating = analysis['rating']
            existing_resume.feedback = analysis['feedback']
            existing_resume.save()
            print(f"Updated MongoResume: {existing_resume.id}, skills: {existing_resume.skills}")

            Log.objects.using('mysql').create(
                user_id=self.request.user.id,
                action="Replaced resume",
                details=f"Resume ID: {existing_resume.id}"
            )

            serializer = self.serializer_class(existing_resume)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            default_storage.delete(new_file_path)
            return Response({'error': f"AI validation failed: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            default_storage.delete(new_file_path)
            return Response({'error': f"Failed to process resume: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)