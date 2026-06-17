from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core import views


router = DefaultRouter()
router.register("educations", views.EducationViewSet, basename="education")
router.register("work-experiences", views.WorkExperienceViewSet, basename="work-experience")
router.register("projects", views.ProjectViewSet, basename="project")
router.register("certifications", views.CertificationViewSet, basename="certification")
router.register("skills", views.SkillViewSet, basename="skill")
router.register("user-skills", views.UserSkillViewSet, basename="user-skill")
router.register("job-sources", views.JobSourceViewSet, basename="job-source")
router.register("external-companies", views.ExternalCompanyViewSet, basename="external-company")
router.register("job-postings", views.JobPostingViewSet, basename="job-posting")
router.register("job-search-criteria", views.JobSearchCriteriaViewSet, basename="job-search-criteria")
router.register("job-matches", views.JobMatchViewSet, basename="job-match")
router.register("salary-benchmarks", views.SalaryBenchmarkViewSet, basename="salary-benchmark")
router.register("salary-recommendations", views.SalaryRecommendationViewSet, basename="salary-recommendation")
router.register("cv-templates", views.CVTemplateViewSet, basename="cv-template")
router.register("generated-cvs", views.GeneratedCVViewSet, basename="generated-cv")
router.register("applications", views.ApplicationViewSet, basename="application")
router.register("interview-preps", views.InterviewPrepViewSet, basename="interview-prep")
router.register("scraping-runs", views.ScrapingRunViewSet, basename="scraping-run")
router.register("ai-logs", views.AIRequestLogViewSet, basename="ai-log")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register/", views.RegisterView.as_view(), name="auth-register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/me/", views.MeView.as_view(), name="me"),
    path("api/profile/", views.ProfileView.as_view(), name="profile"),
    path("api/llm-settings/", views.UserLLMSettingsView.as_view(), name="llm-settings"),
    path("api/llm/chat/", views.UserGroqChatView.as_view(), name="llm-chat"),
    path("api/jobs/<int:pk>/analyze-match/", views.JobAnalyzeMatchView.as_view(), name="job-analyze-match"),
    path("api/jobs/<int:pk>/recommend-salary/", views.JobRecommendSalaryView.as_view(), name="job-recommend-salary"),
    path("api/jobs/<int:pk>/generate-cv/", views.JobGenerateCVView.as_view(), name="job-generate-cv"),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
