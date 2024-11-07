from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.core import serializers
from django.db.models import Q
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

    @action(detail=False)
    def get_all_interview_stages(self, request, pk=None):
        values = InterviewStage.values()
        format_words = lambda words: words.replace("_", " ").title()
        all_values = [(value, format_words(value)) for value in values]
        return Response({'all': all_values})

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

    @action(detail=True, methods=['patch'])
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
        candidate_fields = ["candidate__id", "candidate__name", "candidate__email", "candidate__feedback"]
        candidates_per_interview_stage = {}
        for interview_stage in InterviewStage:
            candidates_info_per_interview_stage = Interview.objects.filter(interview_stage=InterviewStage(interview_stage).value).values_list("id", *candidate_fields)
            candidates_per_interview_stage[interview_stage] = list(candidates_info_per_interview_stage)
        return Response(candidates_per_interview_stage)
    
    @action(detail=True, methods=['get'])
    def get_all_candidates_for_job(self, request, pk=None):
        job_id = pk
        if job_id != 'all':
            all_interview_ids_per_job = Interview.objects.filter(job_id=job_id).values_list("candidate__id", flat=True)
            all_candidates_per_job = Candidate.objects.filter(id__in=all_interview_ids_per_job)
        else:
            all_candidates_per_job = Candidate.objects.all()
        serializer = CandidateSerializer(all_candidates_per_job, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_interview_stages_per_job(self, request, pk=None):
        job_id = pk
        format_words = lambda words: words.replace("_", " ").title()
        interview_stages_per_job_info = {interview_stage.value: {"name": format_words(interview_stage.value), "items": []} 
                                         for interview_stage in InterviewStage}
        queryset = super().get_queryset()
        if job_id != 'all':
            # all_interviews_per_job = base_queryset & Q(job_id=job_id)
            queryset = queryset.filter(Q(job_id=job_id))
        all_interviews_per_job = queryset.values_list(
            "id", "interview_stage", 
            "candidate__id", "candidate__name", "candidate__email", "candidate__feedback")
        for unique_id, interview_and_candidate_info in enumerate(all_interviews_per_job): 
            interview_id, interview_stage, candidate_id, candidate_name, candidate_email, candidate_feedback = interview_and_candidate_info
            candidate_info_item = {'id': str(unique_id), 
                                    'interviewID': str(interview_id),
                                    'candidateID': str(candidate_id), 
                                    'candidateName': candidate_name, 
                                    'candidateEmail': candidate_email,
                                    'candidateFeedback': candidate_feedback}
            interview_stages_per_job_info[interview_stage]["items"].append(candidate_info_item)       
        return Response(interview_stages_per_job_info)    

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    pagination = DefaultPaginator
    serializer_class = JobSerializer

    @action(detail=False)
    def get_archived_jobs(self, request):
        job_data = serializers.serialize('json', list(Job.objects.filter(is_archived=True)))
        return Response(job_data)

