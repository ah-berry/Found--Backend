from rest_framework import serializers
from api.models import Candidate, Interview, Job

class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = "__all__"

class InterviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interview
        fields = "__all__"

class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = "__all__"
