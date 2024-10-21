from rest_framework.routers import DefaultRouter
from api.views import CandidateViewSet, InterviewViewSet, JobViewSet

router = DefaultRouter()
router.register(r'candidate', CandidateViewSet, basename="candidate")
router.register(r'interview', InterviewViewSet, basename='interview')
router.register(r'job', JobViewSet, basename='job')
urlpatterns = router.urls