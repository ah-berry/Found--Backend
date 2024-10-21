from django.db import models
from uuid import uuid4
from enum import Enum

class EmptyStringToNoneField(models.TextField):
    def get_prep_value(self, value):
        if value == '':
            return None
        return value

class InterviewStage(str, Enum):
    APPLICATION_REVIEW = "application_review"
    PRELIMINARY_PHONE_SCREEN = "preliminary_phone_screen"
    PHONE_INTERVIEW = "phone_interview"
    TAKE_HOME_TEST = "take_home_test"
    INTERVIEWS_PASSED = "interviews_passed"

class Candidate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=254)

    # No two candidates with the same email.
    email = models.EmailField(max_length=254, unique=True)
    feedback = models.TextField()

class Interview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    interview_stage = EmptyStringToNoneField(default=InterviewStage.APPLICATION_REVIEW.value, choices=[(tag.value, tag) for tag in InterviewStage])
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, null=False, blank=False, db_index=True)
    job = models.ForeignKey("Job", on_delete=models.CASCADE, null=False, blank=False, db_index=True)

    # Ensures there are no two Interview objects for one Job for a Candidate. Assumes
    # candidate cannot be in two interview stages for the same job at once. 
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["candidate", "job"],
                name="unique_interview_per_job_for_candidate"
            )
        ]

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    is_archived = models.BooleanField(default=False)
 
    
