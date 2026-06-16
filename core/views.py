from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from .models import (
    AIRequestLog,
    Application,
    CVTemplate,
    CandidateProfile,
    Certification,
    Education,
    ExternalCompany,
    GeneratedCV,
    InterviewPrep,
    JobMatch,
    JobPosting,
    JobSearchCriteria,
    JobSource,
    SalaryBenchmark,
    SalaryRecommendation,
    ScrapingRun,
    Skill,
    UserSkill,
    WorkExperience,
    Project,
)
from .serializers import (
    AIRequestLogSerializer,
    ApplicationQuestionSerializer,
    ApplicationSerializer,
    CVTemplateSerializer,
    CandidateProfileSerializer,
    CertificationSerializer,
    EducationSerializer,
    ExternalCompanySerializer,
    GeneratedCVSerializer,
    InterviewPrepSerializer,
    JobMatchSerializer,
    JobPostingSerializer,
    JobSearchCriteriaSerializer,
    JobSourceSerializer,
    RegisterSerializer,
    SalaryBenchmarkSerializer,
    SalaryRecommendationSerializer,
    ScrapingRunSerializer,
    SkillSerializer,
    UserSerializer,
    UserSkillSerializer,
    WorkExperienceSerializer,
    ProjectSerializer,
)
from .services import (
    ApplicationWorkflowService,
    CVGenerationService,
    JobMatchingService,
    SalaryRecommendationService,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ProfileView(APIView):
    def get_object(self, user):
        profile, _ = CandidateProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request):
        serializer = CandidateProfileSerializer(self.get_object(request.user))
        return Response(serializer.data)

    def put(self, request):
        serializer = CandidateProfileSerializer(self.get_object(request.user), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    patch = put


class OwnedViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EducationViewSet(OwnedViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    search_fields = ["institution", "degree", "field_of_study"]
    ordering_fields = ["start_date", "end_date", "created_at"]


class WorkExperienceViewSet(OwnedViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    search_fields = ["company", "position", "description", "tools_used"]
    ordering_fields = ["start_date", "end_date", "created_at"]


class ProjectViewSet(OwnedViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    search_fields = ["name", "description", "technologies", "impact"]


class CertificationViewSet(OwnedViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    search_fields = ["name", "institution", "description"]
    ordering_fields = ["issue_date", "created_at"]


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    search_fields = ["name", "category"]
    filterset_fields = ["category"]


class UserSkillViewSet(OwnedViewSet):
    queryset = UserSkill.objects.select_related("skill")
    serializer_class = UserSkillSerializer
    search_fields = ["skill__name", "level"]
    filterset_fields = ["level", "skill__category"]


class JobSourceViewSet(viewsets.ModelViewSet):
    queryset = JobSource.objects.all()
    serializer_class = JobSourceSerializer
    search_fields = ["name", "source_type"]
    filterset_fields = ["source_type", "is_active"]


class ExternalCompanyViewSet(viewsets.ModelViewSet):
    queryset = ExternalCompany.objects.select_related("source")
    serializer_class = ExternalCompanySerializer
    search_fields = ["name", "industry", "location"]
    filterset_fields = ["source", "industry"]


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.select_related("source", "external_company")
    serializer_class = JobPostingSerializer
    search_fields = ["title", "description", "requirements", "location", "seniority"]
    filterset_fields = ["source", "external_company", "modality", "status", "is_active", "seniority"]
    ordering_fields = ["published_at", "scraped_at", "salary_min", "salary_max", "created_at"]


class JobSearchCriteriaViewSet(OwnedViewSet):
    queryset = JobSearchCriteria.objects.all()
    serializer_class = JobSearchCriteriaSerializer
    filterset_fields = ["modality", "seniority", "is_active"]


class JobMatchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobMatchSerializer
    filterset_fields = ["recommended_to_apply", "job_posting"]
    ordering_fields = ["match_score", "created_at"]

    def get_queryset(self):
        return JobMatch.objects.filter(user=self.request.user).select_related("job_posting")


class SalaryBenchmarkViewSet(viewsets.ModelViewSet):
    queryset = SalaryBenchmark.objects.all()
    serializer_class = SalaryBenchmarkSerializer
    search_fields = ["role", "country", "city", "seniority", "source"]
    filterset_fields = ["country", "city", "seniority", "currency"]


class SalaryRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SalaryRecommendationSerializer
    ordering_fields = ["suggested_salary", "confidence_score", "created_at"]

    def get_queryset(self):
        return SalaryRecommendation.objects.filter(user=self.request.user).select_related("job_posting")


class CVTemplateViewSet(viewsets.ModelViewSet):
    queryset = CVTemplate.objects.all()
    serializer_class = CVTemplateSerializer
    search_fields = ["name"]
    filterset_fields = ["is_default"]


class GeneratedCVViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GeneratedCVSerializer
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        return GeneratedCV.objects.filter(user=self.request.user).select_related("job_posting", "template")


class ApplicationViewSet(OwnedViewSet):
    queryset = Application.objects.select_related("job_posting", "generated_cv", "salary_recommendation")
    serializer_class = ApplicationSerializer
    filterset_fields = ["status", "job_posting"]
    ordering_fields = ["applied_at", "created_at", "updated_at"]

    @action(detail=True, methods=["post"], url_path="generate-answers")
    def generate_answers(self, request, pk=None):
        application = self.get_object()
        questions = request.data.get("questions", [])
        generated = ApplicationWorkflowService.generate_answers(application, questions)
        return Response(ApplicationQuestionSerializer(generated, many=True).data)

    @action(detail=True, methods=["post"], url_path="mark-applied")
    def mark_applied(self, request, pk=None):
        application = ApplicationWorkflowService.mark_applied(self.get_object())
        return Response(self.get_serializer(application).data)

    @action(detail=True, methods=["post"], url_path="generate-interview-prep")
    def generate_interview_prep(self, request, pk=None):
        prep = ApplicationWorkflowService.generate_interview_prep(self.get_object())
        return Response(InterviewPrepSerializer(prep).data, status=status.HTTP_201_CREATED)


class InterviewPrepViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InterviewPrepSerializer
    filterset_fields = ["job_posting", "application"]

    def get_queryset(self):
        return InterviewPrep.objects.filter(user=self.request.user).select_related("job_posting", "application")


class ScrapingRunViewSet(viewsets.ModelViewSet):
    queryset = ScrapingRun.objects.select_related("source")
    serializer_class = ScrapingRunSerializer
    filterset_fields = ["source", "status"]
    ordering_fields = ["started_at", "finished_at", "created_at"]


class AIRequestLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AIRequestLogSerializer
    filterset_fields = ["provider", "model", "task_type"]
    ordering_fields = ["created_at", "tokens_used"]

    def get_queryset(self):
        return AIRequestLog.objects.filter(user=self.request.user)


class JobAnalyzeMatchView(APIView):
    def post(self, request, pk):
        job = get_object_or_404(JobPosting, pk=pk)
        match = JobMatchingService.analyze(request.user, job)
        return Response(JobMatchSerializer(match).data, status=status.HTTP_201_CREATED)


class JobRecommendSalaryView(APIView):
    def post(self, request, pk):
        job = get_object_or_404(JobPosting, pk=pk)
        recommendation = SalaryRecommendationService.recommend(request.user, job)
        return Response(SalaryRecommendationSerializer(recommendation).data, status=status.HTTP_201_CREATED)


class JobGenerateCVView(APIView):
    def post(self, request, pk):
        job = get_object_or_404(JobPosting, pk=pk)
        generated_cv = CVGenerationService.generate(
            request.user,
            job,
            template_id=request.data.get("template"),
        )
        return Response(GeneratedCVSerializer(generated_cv).data, status=status.HTTP_201_CREATED)
