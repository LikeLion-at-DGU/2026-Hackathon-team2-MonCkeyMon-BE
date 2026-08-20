from django.db import models
from experiences.models import ExperienceSession

class Video(models.Model):

    session = models.OneToOneField(
        ExperienceSession, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    video_file = models.FileField(upload_to='videos/')
    is_sms_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Video for Session {self.session.id}"