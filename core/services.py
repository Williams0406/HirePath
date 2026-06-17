from decimal import Decimal

from django.db.models import Q
from django.utils import timezone
from groq import Groq

from .models import (
    AIRequestLog,
    Application,
    ApplicationQuestion,
    CVTemplate,
    GeneratedCV,
    InterviewPrep,
    InterviewQuestion,
    JobMatch,
    JobPosting,
    SalaryBenchmark,
    SalaryRecommendation,
)


class UserGroqService:
    @staticmethod
    def chat(user, messages, task_type="OTHER"):
        settings = getattr(user, "llm_settings", None)
        if not settings or not settings.is_enabled or not settings.groq_api_key:
            raise ValueError("Configura una API key de Groq para este usuario.")

        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=messages,
        )
        content = response.choices[0].message.content if response.choices else ""
        usage = getattr(response, "usage", None)
        tokens_used = getattr(usage, "total_tokens", 0) or 0
        AIRequestLog.objects.create(
            user=user,
            provider="groq",
            model=settings.groq_model,
            task_type=task_type,
            input_data={"messages": messages},
            output_data={"content": content},
            tokens_used=tokens_used,
        )
        return {"content": content, "model": settings.groq_model, "tokens_used": tokens_used}


def _job_text(job):
    return " ".join(
        [
            job.title or "",
            job.description or "",
            job.requirements or "",
            job.responsibilities or "",
            job.seniority or "",
        ]
    ).lower()


class JobMatchingService:
    @staticmethod
    def analyze(user, job):
        user_skills = list(user.user_skills.select_related("skill"))
        job_text = _job_text(job)
        matched = [user_skill.skill.name for user_skill in user_skills if user_skill.skill.name.lower() in job_text]
        missing = []

        keywords = [word.strip(".,;:()[]").lower() for word in job_text.split()]
        technical_terms = sorted({word for word in keywords if len(word) > 3})[:30]
        known = {name.lower() for name in matched}
        for term in technical_terms:
            if term not in known and term in {"python", "django", "react", "next", "sql", "aws", "docker"}:
                missing.append(term)

        total_skill_years = sum((user_skill.years_experience for user_skill in user_skills), Decimal("0"))
        experience_score = min(total_skill_years * Decimal("3"), Decimal("30"))
        skill_score = Decimal("0")
        if user_skills:
            skill_score = Decimal(len(matched)) / Decimal(len(user_skills)) * Decimal("60")

        score = min(skill_score + experience_score + Decimal("10"), Decimal("100")).quantize(Decimal("0.01"))
        explanation = (
            f"Compatibilidad calculada por reglas: {len(matched)} skills encontradas "
            f"y experiencia registrada del candidato."
        )

        match, _ = JobMatch.objects.update_or_create(
            user=user,
            job_posting=job,
            defaults={
                "match_score": score,
                "matched_skills": matched,
                "missing_skills": missing,
                "matched_experience": [],
                "risk_notes": [] if score >= 60 else ["Revisar requisitos antes de postular."],
                "ai_explanation": explanation,
                "recommended_to_apply": score >= 65,
            },
        )
        return match


class SalaryRecommendationService:
    @staticmethod
    def recommend(user, job):
        profile = getattr(user, "candidate_profile", None)
        benchmark_query = Q()
        if job.title:
            benchmark_query |= Q(role__icontains=job.title[:40])
        if job.seniority:
            benchmark_query |= Q(role__icontains=job.seniority)
        benchmarks = SalaryBenchmark.objects.filter(benchmark_query) if benchmark_query else SalaryBenchmark.objects.none()
        if job.salary_min and job.salary_max:
            minimum = job.salary_min
            maximum = job.salary_max
            suggested = (minimum + maximum) / Decimal("2")
            confidence = Decimal("82.00")
            reasoning = "Se uso el rango salarial publicado en la vacante."
            based_on_market = False
        elif benchmarks.exists():
            benchmark = benchmarks.order_by("-collected_at", "-updated_at").first()
            minimum = benchmark.salary_min
            maximum = benchmark.salary_max
            suggested = benchmark.salary_avg or minimum or maximum or Decimal("0")
            confidence = Decimal("72.00")
            reasoning = "Se uso benchmark salarial disponible para un rol similar."
            based_on_market = True
        elif profile and profile.desired_salary_min and profile.desired_salary_max:
            minimum = profile.desired_salary_min
            maximum = profile.desired_salary_max
            suggested = (minimum + maximum) / Decimal("2")
            confidence = Decimal("58.00")
            reasoning = "Se uso la expectativa salarial declarada por el candidato."
            based_on_market = False
        else:
            minimum = None
            maximum = None
            suggested = Decimal("0")
            confidence = Decimal("30.00")
            reasoning = "No hay datos suficientes; se requiere investigacion manual."
            based_on_market = False

        return SalaryRecommendation.objects.create(
            user=user,
            job_posting=job,
            suggested_salary=suggested,
            salary_min_suggested=minimum,
            salary_max_suggested=maximum,
            currency=job.currency,
            reasoning=reasoning,
            confidence_score=confidence,
            based_on_market_data=based_on_market,
        )


class CVGenerationService:
    @staticmethod
    def generate(user, job, template_id=None):
        profile = getattr(user, "candidate_profile", None)
        template = None
        if template_id:
            template = CVTemplate.objects.filter(id=template_id).first()
        if not template:
            template = CVTemplate.objects.filter(is_default=True).first()

        experiences = list(user.work_experiences.order_by("-is_current", "-start_date")[:4])
        projects = list(user.projects.order_by("-updated_at")[:4])
        certifications = list(user.certifications.order_by("-issue_date")[:4])
        skills = list(user.user_skills.select_related("skill").order_by("-years_experience")[:12])
        educations = list(user.educations.order_by("-end_date", "-start_date")[:3])

        summary = profile.professional_summary if profile else ""
        if not summary:
            summary = f"Profesional orientado a aportar valor en {job.title}, con experiencia verificable del perfil."

        generated_cv = GeneratedCV.objects.create(
            user=user,
            job_posting=job,
            template=template,
            professional_summary=summary,
            selected_education=[item.id for item in educations],
            selected_experiences=[item.id for item in experiences],
            selected_projects=[item.id for item in projects],
            selected_certifications=[item.id for item in certifications],
            selected_skills=[item.id for item in skills],
        )
        Application.objects.update_or_create(
            user=user,
            job_posting=job,
            defaults={"generated_cv": generated_cv, "status": "CV_GENERATED"},
        )
        return generated_cv


class ApplicationWorkflowService:
    @staticmethod
    def mark_applied(application):
        application.status = "APPLIED"
        application.applied_at = timezone.now()
        application.save(update_fields=["status", "applied_at", "updated_at"])
        return application

    @staticmethod
    def generate_answers(application, questions):
        created = []
        source_questions = questions or [question.question for question in application.questions.all()]
        if not source_questions:
            source_questions = [
                "Por que eres una buena opcion para este puesto?",
                "Cual es tu expectativa salarial?",
            ]
        for question in source_questions:
            answer = (
                "Respuesta sugerida basada en el perfil real del candidato y los requisitos de la vacante. "
                "Debe revisarse antes de enviar."
            )
            item, _ = ApplicationQuestion.objects.update_or_create(
                application=application,
                question=question,
                defaults={"suggested_answer": answer, "generated_by_ai": False},
            )
            created.append(item)
        return created

    @staticmethod
    def generate_interview_prep(application):
        prep, _ = InterviewPrep.objects.update_or_create(
            user=application.user,
            job_posting=application.job_posting,
            application=application,
            defaults={
                "general_advice": (
                    "Prepara ejemplos concretos con resultados medibles, conecta tu experiencia "
                    "con los requisitos del puesto y evita afirmar experiencia no registrada."
                )
            },
        )
        defaults = [
            ("GENERAL", "Cuentame sobre tu experiencia mas relevante para este puesto."),
            ("TECHNICAL", "Que herramientas usarias para resolver los retos principales del rol?"),
            ("BEHAVIORAL", "Describe una situacion dificil y como la resolviste."),
            ("SALARY", "Cual es tu expectativa salarial y como la sustentarias?"),
            ("COMPANY_FIT", "Por que te interesa esta empresa o vacante?"),
        ]
        for category, question in defaults:
            InterviewQuestion.objects.update_or_create(
                interview_prep=prep,
                question=question,
                defaults={
                    "category": category,
                    "suggested_answer": "Construir respuesta con informacion verdadera del perfil y la vacante.",
                },
            )
        return prep
