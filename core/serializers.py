from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import (
    AIRequestLog,
    Application,
    ApplicationQuestion,
    CVTemplate,
    CandidateProfile,
    Certification,
    Education,
    ExternalCompany,
    GeneratedCV,
    InterviewPrep,
    InterviewQuestion,
    JobMatch,
    JobPosting,
    JobSearchCriteria,
    JobSource,
    SalaryBenchmark,
    SalaryRecommendation,
    ScrapedPageLog,
    ScrapingRun,
    Skill,
    UserSkill,
    WorkExperience,
    Project,
)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        CandidateProfile.objects.create(user=user)
        return user


class CandidateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CandidateProfile
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class OwnedModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class EducationSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Education


class WorkExperienceSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = WorkExperience


class ProjectSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Project


class CertificationSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Certification


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class UserSkillSerializer(OwnedModelSerializer):
    skill_detail = SkillSerializer(source="skill", read_only=True)
    skill_name = serializers.CharField(write_only=True, required=False, allow_blank=False)
    skill_category = serializers.CharField(write_only=True, required=False, default="OTHER")

    class Meta(OwnedModelSerializer.Meta):
        model = UserSkill
        fields = [
            "id",
            "user",
            "skill",
            "skill_detail",
            "skill_name",
            "skill_category",
            "level",
            "years_experience",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
        extra_kwargs = {"skill": {"required": False}}

    def validate(self, attrs):
        if not attrs.get("skill") and not attrs.get("skill_name"):
            raise serializers.ValidationError("Debe enviar skill o skill_name.")
        return attrs

    def create(self, validated_data):
        skill_name = validated_data.pop("skill_name", None)
        skill_category = validated_data.pop("skill_category", "OTHER")
        if skill_name:
            skill, _ = Skill.objects.get_or_create(
                name=skill_name.strip(),
                defaults={"category": skill_category},
            )
            validated_data["skill"] = skill
        return super().create(validated_data)


class JobSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSource
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class ExternalCompanySerializer(serializers.ModelSerializer):
    source_detail = JobSourceSerializer(source="source", read_only=True)

    class Meta:
        model = ExternalCompany
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class JobPostingSerializer(serializers.ModelSerializer):
    source_detail = JobSourceSerializer(source="source", read_only=True)
    external_company_detail = ExternalCompanySerializer(source="external_company", read_only=True)

    class Meta:
        model = JobPosting
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class JobSearchCriteriaSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = JobSearchCriteria


class JobMatchSerializer(serializers.ModelSerializer):
    job_posting_detail = JobPostingSerializer(source="job_posting", read_only=True)

    class Meta:
        model = JobMatch
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class SalaryBenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryBenchmark
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class SalaryRecommendationSerializer(serializers.ModelSerializer):
    job_posting_detail = JobPostingSerializer(source="job_posting", read_only=True)

    class Meta:
        model = SalaryRecommendation
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class CVTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVTemplate
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class GeneratedCVSerializer(serializers.ModelSerializer):
    job_posting_detail = JobPostingSerializer(source="job_posting", read_only=True)
    template_detail = CVTemplateSerializer(source="template", read_only=True)

    class Meta:
        model = GeneratedCV
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class ApplicationQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationQuestion
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class ApplicationSerializer(serializers.ModelSerializer):
    job_posting_detail = JobPostingSerializer(source="job_posting", read_only=True)
    questions = ApplicationQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class InterviewPrepSerializer(serializers.ModelSerializer):
    questions = InterviewQuestionSerializer(many=True, read_only=True)
    job_posting_detail = JobPostingSerializer(source="job_posting", read_only=True)

    class Meta:
        model = InterviewPrep
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class ScrapedPageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedPageLog
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class ScrapingRunSerializer(serializers.ModelSerializer):
    page_logs = ScrapedPageLogSerializer(many=True, read_only=True)

    class Meta:
        model = ScrapingRun
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class AIRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRequestLog
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]
