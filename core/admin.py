from django.contrib import admin

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


models = [
    CandidateProfile,
    Education,
    WorkExperience,
    Project,
    Certification,
    Skill,
    UserSkill,
    JobSource,
    ExternalCompany,
    JobPosting,
    JobSearchCriteria,
    JobMatch,
    SalaryBenchmark,
    SalaryRecommendation,
    CVTemplate,
    GeneratedCV,
    Application,
    ApplicationQuestion,
    InterviewPrep,
    InterviewQuestion,
    ScrapingRun,
    ScrapedPageLog,
    AIRequestLog,
]

for model in models:
    admin.site.register(model)
