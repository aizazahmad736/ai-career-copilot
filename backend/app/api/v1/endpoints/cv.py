from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
import os

from app.core.database import get_db
from app.models.resume import Resume
from app.models.analysis import ResumeAnalysis
from app.schemas.analysis import SkillGapAnalysisResponse, ATSFeedback, SkillMatchItem, ActionableRecommendation
from app.schemas.resume import ParsedResumeData, PersonalInfo, CategorizedSkills, WorkExperience, EducationItem, ProjectItem
from app.services.parser_service import parser_service
from app.services.gemini_service import gemini_service
from app.services.skill_gap_service import skill_gap_service, ROLE_BENCHMARKS

router = APIRouter()

@router.get("/roles")
def get_supported_roles():
    roles = []
    for role_name, data in ROLE_BENCHMARKS.items():
        roles.append({
            "name": role_name,
            "critical_skill_count": len(data["critical"]),
            "recommended_skill_count": len(data["recommended"]),
            "sample_skills": [s["skill"] for s in data["critical"][:4]]
        })
    return {"roles": roles}

@router.post("/analyze", response_model=SkillGapAnalysisResponse)
async def analyze_cv(
    file: UploadFile = File(...),
    target_role: str = Form("Junior Full Stack Developer"),
    target_experience_level: str = Form("Entry-Level / Junior"),
    job_description: Optional[str] = Form(None),
    custom_gemini_api_key: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # 1. Read file bytes
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read uploaded file: {str(e)}")

    if len(contents) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File size exceeds maximum allowed 10MB limit.")

    # 2. Parse text from document
    try:
        raw_text, file_type = parser_service.parse_file(contents, file.filename or "uploaded_resume.pdf")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume document: {str(e)}")

    # 3. Store resume raw record in DB
    resume_record = Resume(
        filename=file.filename or "resume",
        file_type=file_type,
        file_size_bytes=len(contents),
        raw_text=raw_text
    )
    db.add(resume_record)
    db.commit()
    db.refresh(resume_record)

    # 4. AI Analysis via Gemini
    ai_result = gemini_service.analyze_resume_text(raw_text, custom_api_key=custom_gemini_api_key)

    # 5. Extract and normalize skills
    skills_data = ai_result.get("skills", {})

    # 6. Skill Gap Analysis
    match_score, matched, partial, missing, bonus, recommendations = skill_gap_service.evaluate_gaps(
        extracted_skills=skills_data,
        target_role=target_role,
        job_description=job_description
    )

    # 7. Persist analysis results
    personal_info = ai_result.get("personal_info", {})
    candidate_name = personal_info.get("name", "Candidate")
    candidate_email = personal_info.get("email")

    analysis_record = ResumeAnalysis(
        resume_id=resume_record.id,
        target_role=target_role,
        experience_level=target_experience_level,
        match_score=match_score,
        candidate_name=candidate_name,
        candidate_email=candidate_email,
        headline=ai_result.get("professional_headline"),
        summary=ai_result.get("executive_summary"),
        extracted_skills=skills_data,
        matched_skills=[m.model_dump() for m in matched],
        partial_skills=[p.model_dump() for p in partial],
        missing_skills=[m.model_dump() for m in missing],
        bonus_skills=[b.model_dump() for b in bonus],
        recommendations=[r.model_dump() for r in recommendations],
        ats_feedback=ai_result.get("ats_feedback", {})
    )
    db.add(analysis_record)
    db.commit()
    db.refresh(analysis_record)

    # 8. Build response
    parsed_resume = ParsedResumeData(
        personal_info=PersonalInfo(**personal_info),
        professional_headline=ai_result.get("professional_headline"),
        executive_summary=ai_result.get("executive_summary"),
        skills=CategorizedSkills(**skills_data),
        experience=[WorkExperience(**exp) for exp in ai_result.get("experience", [])],
        education=[EducationItem(**edu) for edu in ai_result.get("education", [])],
        projects=[ProjectItem(**proj) for proj in ai_result.get("projects", [])],
        certifications=ai_result.get("certifications", [])
    )

    ats_fb = ai_result.get("ats_feedback", {})
    ats_feedback_obj = ATSFeedback(
        overall_ats_score=ats_fb.get("overall_ats_score", 75),
        readability_score=ats_fb.get("readability_score", 80),
        impact_metrics_score=ats_fb.get("impact_metrics_score", 65),
        strengths=ats_fb.get("strengths", []),
        weaknesses=ats_fb.get("weaknesses", []),
        actionable_bullet_fixes=ats_fb.get("actionable_bullet_fixes", [])
    )

    return SkillGapAnalysisResponse(
        id=analysis_record.id,
        target_role=target_role,
        experience_level=target_experience_level,
        match_score=match_score,
        candidate_name=candidate_name,
        headline=ai_result.get("professional_headline"),
        summary=ai_result.get("executive_summary"),
        parsed_resume=parsed_resume,
        matched_skills=matched,
        partial_skills=partial,
        missing_critical_skills=missing,
        bonus_skills=bonus,
        ats_feedback=ats_feedback_obj,
        recommendations=recommendations,
        is_demo_mode=ai_result.get("is_demo_mode", False)
    )

@router.post("/analyze-sample", response_model=SkillGapAnalysisResponse)
async def analyze_sample_resume(
    target_role: str = Form("Junior Full Stack Developer"),
    target_experience_level: str = Form("Entry-Level / Junior"),
    job_description: Optional[str] = Form(None),
    custom_gemini_api_key: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    sample_path = os.path.join(os.path.dirname(__file__), "../../../samples/sample_resume.txt")
    if os.path.exists(sample_path):
        with open(sample_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
    else:
        raw_text = "Alex Chen\nalex.chen@email.com\nSkills: Python, JavaScript, React, FastAPI, PostgreSQL, Git, Docker"

    # AI Analysis
    ai_result = gemini_service.analyze_resume_text(raw_text, custom_api_key=custom_gemini_api_key)
    skills_data = ai_result.get("skills", {})

    # Skill Gap
    match_score, matched, partial, missing, bonus, recommendations = skill_gap_service.evaluate_gaps(
        extracted_skills=skills_data,
        target_role=target_role,
        job_description=job_description
    )

    personal_info = ai_result.get("personal_info", {})
    candidate_name = personal_info.get("name", "Alex Chen")

    parsed_resume = ParsedResumeData(
        personal_info=PersonalInfo(**personal_info),
        professional_headline=ai_result.get("professional_headline", "Aspiring Full-Stack Software Engineer"),
        executive_summary=ai_result.get("executive_summary", "Motivated CS graduate proficient in modern web stacks."),
        skills=CategorizedSkills(**skills_data),
        experience=[WorkExperience(**exp) for exp in ai_result.get("experience", [])],
        education=[EducationItem(**edu) for edu in ai_result.get("education", [])],
        projects=[ProjectItem(**proj) for proj in ai_result.get("projects", [])],
        certifications=ai_result.get("certifications", [])
    )

    ats_fb = ai_result.get("ats_feedback", {})
    ats_feedback_obj = ATSFeedback(
        overall_ats_score=ats_fb.get("overall_ats_score", 82),
        readability_score=ats_fb.get("readability_score", 85),
        impact_metrics_score=ats_fb.get("impact_metrics_score", 70),
        strengths=ats_fb.get("strengths", ["Strong project experience with modern stack", "Clear education and skill breakdown"]),
        weaknesses=ats_fb.get("weaknesses", ["Could add more percentage metrics to bullet points"]),
        actionable_bullet_fixes=ats_fb.get("actionable_bullet_fixes", [])
    )

    return SkillGapAnalysisResponse(
        id=999,
        target_role=target_role,
        experience_level=target_experience_level,
        match_score=match_score,
        candidate_name=candidate_name,
        headline=ai_result.get("professional_headline"),
        summary=ai_result.get("executive_summary"),
        parsed_resume=parsed_resume,
        matched_skills=matched,
        partial_skills=partial,
        missing_critical_skills=missing,
        bonus_skills=bonus,
        ats_feedback=ats_feedback_obj,
        recommendations=recommendations,
        is_demo_mode=ai_result.get("is_demo_mode", False)
    )
