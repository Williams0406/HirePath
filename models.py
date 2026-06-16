from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CandidateProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_profile"
    )
    headline = models.CharField(max_length=255, blank=True)
    professional_summary = models.TextField(blank=True)
    years_experience = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    current_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    desired_salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    desired_salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    availability = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    def __str__(self):
        return f"Perfil de {self.user}"


class Education(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="educations")
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class WorkExperience(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="work_experiences")
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    tools_used = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} - {self.company}"


class Project(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)
    description = models.TextField()
    technologies = models.TextField(blank=True)
    impact = models.TextField(blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Certification(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certifications")
    name = models.CharField(max_length=255)
    institution = models.CharField(max_length=255, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Skill(TimeStampedModel):
    CATEGORY_CHOICES = [
        ("TECHNICAL", "Técnica"),
        ("SOFT", "Blanda"),
        ("LANGUAGE", "Idioma"),
        ("TOOL", "Herramienta"),
        ("OTHER", "Otra"),
    ]

    name = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="OTHER")

    def __str__(self):
        return self.name


class UserSkill(TimeStampedModel):
    LEVEL_CHOICES = [
        ("BASIC", "Básico"),
        ("INTERMEDIATE", "Intermedio"),
        ("ADVANCED", "Avanzado"),
        ("EXPERT", "Experto"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="user_skills")
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default="BASIC")
    years_experience = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    class Meta:
        unique_together = ("user", "skill")

    def __str__(self):
        return f"{self.user} - {self.skill}"


class JobSource(TimeStampedModel):
    SOURCE_TYPE_CHOICES = [
        ("LINKEDIN", "LinkedIn"),
        ("COMPUTRABAJO", "Computrabajo"),
        ("BUMERAN", "Bumeran"),
        ("INDEED", "Indeed"),
        ("COMPANY_SITE", "Página corporativa"),
        ("OTHER", "Otro"),
    ]

    name = models.CharField(max_length=150)
    base_url = models.URLField()
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ExternalCompany(TimeStampedModel):
    source = models.ForeignKey(JobSource, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class JobPosting(TimeStampedModel):
    MODALITY_CHOICES = [
        ("ONSITE", "Presencial"),
        ("REMOTE", "Remoto"),
        ("HYBRID", "Híbrido"),
        ("UNKNOWN", "No especificado"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Activa"),
        ("EXPIRED", "Expirada"),
        ("CLOSED", "Cerrada"),
        ("UNKNOWN", "No especificada"),
    ]

    source = models.ForeignKey(JobSource, on_delete=models.SET_NULL, null=True, blank=True)
    external_company = models.ForeignKey(
        ExternalCompany,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_postings"
    )

    external_job_id = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)

    location = models.CharField(max_length=255, blank=True)
    modality = models.CharField(max_length=50, choices=MODALITY_CHOICES, default="UNKNOWN")
    contract_type = models.CharField(max_length=100, blank=True)
    seniority = models.CharField(max_length=100, blank=True)

    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_text = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=10, default="PEN")

    url = models.URLField(max_length=1000, unique=True)
    published_at = models.DateTimeField(null=True, blank=True)
    scraped_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="ACTIVE")
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["location"]),
            models.Index(fields=["seniority"]),
            models.Index(fields=["source"]),
        ]

    def __str__(self):
        return self.title


class JobSearchCriteria(TimeStampedModel):
    MODALITY_CHOICES = JobPosting.MODALITY_CHOICES

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_search_criteria")

    target_roles = models.JSONField(default=list, blank=True)
    keywords = models.JSONField(default=list, blank=True)
    excluded_keywords = models.JSONField(default=list, blank=True)
    locations = models.JSONField(default=list, blank=True)
    industries = models.JSONField(default=list, blank=True)

    modality = models.CharField(max_length=50, choices=MODALITY_CHOICES, default="UNKNOWN")
    seniority = models.CharField(max_length=100, blank=True)
    salary_min_expected = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    max_applications_per_day = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Criterios de {self.user}"


class JobMatch(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_matches")
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="matches")

    match_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    matched_experience = models.JSONField(default=list, blank=True)
    risk_notes = models.JSONField(default=list, blank=True)

    ai_explanation = models.TextField(blank=True)
    recommended_to_apply = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "job_posting")

    def __str__(self):
        return f"{self.user} - {self.job_posting} - {self.match_score}%"


class SalaryBenchmark(TimeStampedModel):
    role = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    seniority = models.CharField(max_length=100, blank=True)

    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    currency = models.CharField(max_length=10, default="PEN")
    source = models.CharField(max_length=255, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.role} - {self.city} - {self.salary_avg}"


class SalaryRecommendation(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="salary_recommendations")
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="salary_recommendations")

    suggested_salary = models.DecimalField(max_digits=10, decimal_places=2)
    salary_min_suggested = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max_suggested = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    currency = models.CharField(max_length=10, default="PEN")
    reasoning = models.TextField(blank=True)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    based_on_user_experience = models.BooleanField(default=True)
    based_on_job_seniority = models.BooleanField(default=True)
    based_on_market_data = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.job_posting} - {self.suggested_salary}"


class CVTemplate(TimeStampedModel):
    name = models.CharField(max_length=150)
    html_structure = models.TextField()
    css_styles = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GeneratedCV(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="generated_cvs")
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="generated_cvs")
    template = models.ForeignKey(CVTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    professional_summary = models.TextField(blank=True)

    selected_education = models.JSONField(default=list, blank=True)
    selected_experiences = models.JSONField(default=list, blank=True)
    selected_projects = models.JSONField(default=list, blank=True)
    selected_certifications = models.JSONField(default=list, blank=True)
    selected_skills = models.JSONField(default=list, blank=True)

    pdf_file = models.FileField(upload_to="generated_cvs/", null=True, blank=True)

    def __str__(self):
        return f"CV de {self.user} para {self.job_posting}"


class Application(TimeStampedModel):
    STATUS_CHOICES = [
        ("DETECTED", "Detectada"),
        ("MATCHED", "Compatible"),
        ("CV_GENERATED", "CV generado"),
        ("PENDING_REVIEW", "Pendiente de revisión"),
        ("APPLIED", "Postulada"),
        ("INTERVIEW", "Entrevista"),
        ("REJECTED", "Rechazada"),
        ("OFFER", "Oferta recibida"),
        ("HIRED", "Contratado"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="applications")

    generated_cv = models.ForeignKey(
        GeneratedCV,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications"
    )

    salary_recommendation = models.ForeignKey(
        SalaryRecommendation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications"
    )

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="DETECTED")
    application_url = models.URLField(max_length=1000, blank=True)
    applied_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "job_posting")

    def __str__(self):
        return f"{self.user} - {self.job_posting} - {self.status}"


class ApplicationQuestion(TimeStampedModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="questions")

    question = models.TextField()
    suggested_answer = models.TextField(blank=True)
    final_answer = models.TextField(blank=True)

    generated_by_ai = models.BooleanField(default=True)
    reviewed_by_user = models.BooleanField(default=False)

    def __str__(self):
        return self.question[:80]


class InterviewPrep(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interview_preps")
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="interview_preps")
    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interview_preps"
    )

    general_advice = models.TextField(blank=True)

    def __str__(self):
        return f"Entrevista - {self.user} - {self.job_posting}"


class InterviewQuestion(TimeStampedModel):
    CATEGORY_CHOICES = [
        ("GENERAL", "General"),
        ("TECHNICAL", "Técnica"),
        ("BEHAVIORAL", "Conductual"),
        ("SALARY", "Salario"),
        ("COMPANY_FIT", "Afinidad con la empresa"),
    ]

    interview_prep = models.ForeignKey(InterviewPrep, on_delete=models.CASCADE, related_name="questions")

    question = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="GENERAL")
    suggested_answer = models.TextField(blank=True)
    user_notes = models.TextField(blank=True)

    def __str__(self):
        return self.question[:80]


class ScrapingRun(TimeStampedModel):
    STATUS_CHOICES = [
        ("PENDING", "Pendiente"),
        ("RUNNING", "Ejecutando"),
        ("SUCCESS", "Exitoso"),
        ("FAILED", "Fallido"),
        ("PARTIAL", "Parcial"),
    ]

    source = models.ForeignKey(JobSource, on_delete=models.CASCADE, related_name="scraping_runs")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    jobs_found = models.PositiveIntegerField(default=0)
    jobs_created = models.PositiveIntegerField(default=0)
    jobs_updated = models.PositiveIntegerField(default=0)

    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.source} - {self.status}"


class ScrapedPageLog(TimeStampedModel):
    scraping_run = models.ForeignKey(ScrapingRun, on_delete=models.CASCADE, related_name="page_logs")

    url = models.URLField(max_length=1000)
    status_code = models.PositiveIntegerField(null=True, blank=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    scraped_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.url


class AIRequestLog(TimeStampedModel):
    TASK_TYPE_CHOICES = [
        ("JOB_MATCH", "Compatibilidad con puesto"),
        ("CV_GENERATION", "Generación de CV"),
        ("SALARY_RECOMMENDATION", "Recomendación salarial"),
        ("APPLICATION_ANSWER", "Respuesta de postulación"),
        ("INTERVIEW_PREP", "Preparación de entrevista"),
        ("OTHER", "Otro"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ai_logs"
    )

    provider = models.CharField(max_length=100, default="groq")
    model = models.CharField(max_length=150, blank=True)
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES, default="OTHER")

    input_data = models.JSONField(default=dict, blank=True)
    output_data = models.JSONField(default=dict, blank=True)

    tokens_used = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.provider} - {self.task_type}"