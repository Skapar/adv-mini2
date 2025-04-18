from django.contrib import admin
from .models import JobDescription, Log, MongoResumeProxy
from .models import MongoResume

@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'recruiter', 'description', 'required_skills', 'required_experience', 'created_at')
    list_filter = ('created_at', 'recruiter')
    search_fields = ('description', 'required_skills', 'required_experience')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'action', 'details', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('action', 'details')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

@admin.register(MongoResumeProxy)
class MongoResumeProxyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'file', 'skills', 'experience', 'education', 'rating', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('skills', 'experience', 'education')
    date_hierarchy = 'uploaded_at'
    ordering = ('-uploaded_at',)

    def get_queryset(self, request):
        resumes = MongoResume.objects.all()
        return [
            {
                'id': str(resume.id),
                'user_id': resume.user_id,
                'file': resume.file,
                'skills': resume.skills or '',
                'experience': resume.experience or '',
                'education': resume.education or '',
                'rating': resume.rating,
                'feedback': resume.feedback,
                'uploaded_at': resume.uploaded_at,
            }
            for resume in resumes
        ]

    def get_object(self, request, object_id, from_field=None):
        resume = MongoResume.objects.get(id=object_id)
        return MongoResumeProxy(
            id=str(resume.id),
            user_id=resume.user_id,
            file=resume.file,
            skills=resume.skills or '',
            experience=resume.experience or '',
            education=resume.education or '',
            rating=resume.rating,
            feedback=resume.feedback,
            uploaded_at=resume.uploaded_at,
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True