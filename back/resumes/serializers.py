from rest_framework import serializers
from .models import Resume, JobDescription
class ResumeSerializer(serializers.Serializer):
    id = serializers.CharField(source='id.__str__', read_only=True)
    file = serializers.CharField(read_only=True)
    uploaded_at = serializers.DateTimeField(read_only=True)
    skills = serializers.CharField(read_only=True)
    experience = serializers.CharField(read_only=True)
    education = serializers.CharField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    analysis = serializers.SerializerMethodField()

    def get_analysis(self, obj):
        return {
            'skills': obj.skills,
            'experience': obj.experience,
            'education': obj.education,
            'rating': float(obj.rating) if obj.rating is not None else 0.0,
            'feedback': obj.feedback
        }

    def create(self, validated_data):
        return validated_data

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ['id', 'description', 'required_skills', 'required_experience', 'created_at']
        read_only_fields = ['required_skills', 'required_experience', 'created_at']