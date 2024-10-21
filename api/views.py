from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.core import serializers
from api.pagination import DefaultPaginator
from api.serializer import CandidateSerializer, InterviewSerializer, JobSerializer
from api.models import Candidate, Interview, Job, InterviewStage

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    pagination = DefaultPaginator
    serializer_class = CandidateSerializer

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    pagination = DefaultPaginator
    serializer_class = InterviewSerializer

    @action(detail=True, methods=['post'])
    def assign_candidate_to_job(self, request, pk=None):
        candidate_id = pk
        job_id = self.request.data.get("job_id")

        interview = Interview.objects.filter(candidate_id=candidate_id, job_id=job_id)
        # Assign candidate to target job by creating an associated Interview object.
        # Assigning a new candidate to a job automatically adopts the first stage of 
        # the interview (APPLICATION_REVIEW). 
        if not interview.exists():
            new_interview = Interview.objects.create(
                candidate_id=candidate_id, 
                job_id=job_id)
            new_interview.save()
        else:
            # This means a candidate is already assigned to this job.
            # Return error response from backend and prevent reassigning
            # a candidate to the same job.
            raise ValidationError("Candidate is already assigned to this job and is interviewing.")
        return Response({'RESPONSE SUCCESSFUL': True})

    @action(detail=True, methods=['post'])
    def assign_candidate_to_interview_stage(self, request, pk=None):
        candidate_id = pk
        interview_id = self.request.data.get("interview_id")
        target_interview_stage = self.request.data.get("target_interview_stage")

        interviews = Interview.objects.filter(id=interview_id, candidate_id=candidate_id)

        if interviews.exists():
            # Assumes only one Interview object fulfills this interview_id and candidate_id
            # criteria.
            interview = interviews[0]
            interview.interview_stage = InterviewStage(target_interview_stage).value
            interview.save()
        else:
            # This means the frontend provided a job the candidate isn't interviewing for and 
            # attempting to move them to a different interview stage.
            raise ValidationError("Candidate is not assigned to this job and is not interviewing.")
        return Response({'RESPONSE SUCCESSFUL': True})

    @action(detail=False)
    def get_all_candidates_per_interview_stage(self, request, pk=None):
        candidate_fields = ["candidate__name", "candidate__email", "candidate__feedback"]
        candidates_per_interview_stage = {}
        for interview_stage in InterviewStage:
            candidates_info_per_interview_stage = Interview.objects.filter(interview_stage=InterviewStage(interview_stage).value).values_list(*candidate_fields)
            candidates_per_interview_stage[interview_stage] = list(candidates_info_per_interview_stage)
        return Response(candidates_per_interview_stage)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    pagination = DefaultPaginator
    serializer_class = JobSerializer

    @action(detail=False)
    def get_archived_jobs(self, request):
        job_data = serializers.serialize('json', list(Job.objects.filter(is_archived=True)))
        return Response(job_data)

