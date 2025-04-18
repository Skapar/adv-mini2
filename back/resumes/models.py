
from django.db import models
from mongoengine import Document, fields
from users.models import CustomUser
import json
from django.utils import timezone

class Resume(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    rating = models.FloatField(null=True, blank=True)
    recommendations = models.TextField(blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        db_table = 'resumes'

    def set_feedback(self, feedback_dict):
        self.feedback = json.dumps(feedback_dict)

    def get_feedback(self):
        return json.loads(self.feedback) if self.feedback else {}

    def __str__(self):
        return f"{self.user.username}'s resume"

class MongoResume(Document):
    user_id = fields.IntField(required=True)
    file = fields.StringField(required=True)
    uploaded_at = fields.DateTimeField(default=lambda: timezone.now())
    skills = fields.StringField(default='')
    experience = fields.StringField(default='')
    education = fields.StringField(default='')
    rating = fields.FloatField(default=0.0)
    feedback = fields.DictField(default={})

    meta = {
        'collection': 'resumes'
    }

class JobDescription(models.Model):
    recruiter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'recruiter'})
    description = models.TextField()
    required_skills = models.TextField(blank=True)
    required_experience = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job by {self.recruiter.username} - {self.created_at}"

class Log(models.Model):
    user_id = models.IntegerField()
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    class Meta:
        db_table = 'logs'

    def __str__(self):
        return f"User {self.user_id} - {self.action} - {self.timestamp}"

class MongoResumeProxy(models.Model):
    class Meta:
        managed = False
        verbose_name = 'Mongo Resume'
        verbose_name_plural = 'Mongo Resumes'

    id = models.CharField(max_length=24, primary_key=True)
    user_id = models.IntegerField()
    file = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField()
    skills = models.CharField(max_length=500, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=500, blank=True)
    rating = models.FloatField(blank=True, null=True)
    feedback = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Resume {self.id} (User {self.user_id})"