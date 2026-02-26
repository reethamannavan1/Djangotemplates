from django.shortcuts import render

def resume_home(request):
    return render(request, "resumes/home.html")


# resumes/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now

from .models import ResumeOptimization
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@login_required
def resume_optimizer(request):

    # ⭐ PLAN CHECK
    if request.user.plan.name == "Starter":
        messages.error(request, "Resume optimization is available for Pro users.")
        return redirect("pricing")

    ai_result = None
    optimized_resume = None

    if request.method == "POST":

        resume_text = request.POST.get("resume_text")
        job_desc = request.POST.get("job_desc")

        # ⭐ file upload support
        if "resume_file" in request.FILES:
            uploaded_file = request.FILES["resume_file"]
            resume_text = uploaded_file.read().decode("utf-8", errors="ignore")

        if not resume_text:
            messages.error(request, "Please paste or upload a resume.")
            return redirect("resume-optimizer")

        resume_text = resume_text[:3000]
        job_desc = (job_desc or "")[:3000]

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an ATS resume optimization engine."},
                {
                    "role": "user",
                    "content": f"""
Optimize this resume for ATS.

RESUME:
{resume_text}

JOB:
{job_desc}

Return:

ATS SCORE
MISSING KEYWORDS
IMPROVEMENTS
OPTIMIZED RESUME
"""
                }
            ],
            model="openai/gpt-oss-20b"
        )

        ai_result = response.choices[0].message.content

        if ai_result and "OPTIMIZED RESUME" in ai_result:
            optimized_resume = ai_result.split("OPTIMIZED RESUME", 1)[1].strip()

        # ⭐ usage tracking
        ResumeOptimization.objects.create(user=request.user)

    return render(request, "resumes/optimizer.html", {
        "ai_result": ai_result,
        "optimized_resume": optimized_resume
    })





from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io


def download_optimized_resume_pdf(request):

    data = request.GET.get("data", "")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    # ⭐ custom styles
    heading = ParagraphStyle(
        name="Heading",
        parent=styles["Heading2"],
        spaceAfter=8,
        spaceBefore=14
    )

    normal = styles["Normal"]

    elements = []

    # ⭐ App title
    elements.append(Paragraph("Resume AI — Optimized Resume", styles["Title"]))
    elements.append(Spacer(1, 20))

    # ⭐ Clean HTML breaks
    clean = data.replace("<br>", "<br />")

    # ⭐ Split sections
    lines = clean.split("\n")

    for line in lines:

        if not line.strip():
            elements.append(Spacer(1, 6))
            continue

        # ⭐ detect headings
        if line.isupper() and len(line) < 40:
            elements.append(Paragraph(line, heading))
        else:
            elements.append(Paragraph(line, normal))

        elements.append(Spacer(1, 4))

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="optimized_resume.pdf"'

    return response






#templatesview

from .models import Template, UserTemplate
@login_required
def templates(request):

    resume_templates = Template.objects.filter(type="resume")

    user_owned = UserTemplate.objects.filter(user=request.user).values_list("template_id", flat=True)

    return render(request, "resumes/templates.html", {
        "templates": resume_templates,
        "owned": user_owned
    })


@login_required
def preview_template(request, pk):
    template = get_object_or_404(Template, pk=pk)
    return render(request, "resumes/template_preview.html", {"template": template})



@login_required
def use_template(request, pk):

    template = get_object_or_404(Template, pk=pk)

    # ⭐ FREE TEMPLATE
    if template.is_free:
        UserTemplate.objects.get_or_create(user=request.user, template=template)
        return redirect("create_resume")

    # ⭐ PREMIUM TEMPLATE
    if request.user.plan.name == "Starter":
        messages.warning(request, "Upgrade to use premium templates")
        return redirect("pricing")

    # ⭐ PRO USER
    UserTemplate.objects.get_or_create(user=request.user, template=template)

    return redirect("create_resume")








#createresume
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Resume
from services.ai_service import ask_ai


# ⭐ LIST
@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "resumes/list.html", {"resumes": resumes})




@login_required
def create_resume(request):

    # ⭐ STARTER LIMIT
    if request.user.plan.name == "Starter":
        count = Resume.objects.filter(user=request.user).count()
        if count >= 1:
            messages.warning(request, "Starter plan allows only 1 resume. Upgrade to create more.")
            return redirect("pricing")

    ai_data = None

    # ⭐ GENERATE
    if request.method == "POST" and "generate" in request.POST:

        role = request.POST.get("role")
        experience = request.POST.get("experience")
        skills = request.POST.get("skills")
        notes = request.POST.get("notes")

        # store for save
        request.session["resume_role"] = role

        prompt = f"""
Create ATS ready resume.

ROLE: {role}
EXPERIENCE: {experience}
SKILLS: {skills}
NOTES: {notes}
"""

        ai_data = ask_ai(prompt)

    # ⭐ SAVE
    if request.method == "POST" and "save" in request.POST:

        role = request.session.get("resume_role", "AI Resume")
        content = request.POST.get("content")

        Resume.objects.create(
            user=request.user,
            title=f"{role} Resume",
            summary=content
        )

        messages.success(request, "Resume saved successfully")
        return redirect("resume-list")

    return render(request, "resumes/create.html", {"ai_data": ai_data})




# ⭐ DELETE
@login_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    resume.delete()
    messages.success(request, "Resume deleted")
    return redirect("resume-list")


#coverletter

from .models import CoverLetter
@login_required
def cover_letter(request):

    # ⭐ FEATURE LIMITATION (PUT HERE)
    if request.user.plan.name == "Starter":
        messages.warning(request, "Cover Letter Generator is available for Pro users.")
        return redirect("pricing")

    letter = None

    if request.method == "POST":

        resume_text = request.POST.get("resume_text")
        job_title = request.POST.get("job_title")
        company = request.POST.get("company")

        response = client.chat.completions.create(
            messages=[
                {"role":"system","content":"You are a professional cover letter writer."},
                {"role":"user","content":f"""
Write a professional cover letter.

Job title: {job_title}
Company: {company}

Resume:
{resume_text}

Make it concise and engaging.
"""}
            ],
            model="openai/gpt-oss-20b"
        )

        letter = response.choices[0].message.content
        CoverLetter.objects.create(user=request.user, content=letter)

    return render(request,"resumes/cover_letter.html",{"letter":letter})






from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

@login_required
def download_cover_letter_pdf(request):
    data = request.GET.get("data", "")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(name="Title", fontSize=18, spaceAfter=12, alignment=1)
    normal_style = styles["Normal"]

    elements = []

    elements.append(Paragraph("Resume AI", title_style))
    elements.append(Spacer(1, 12))

    clean_data = data.replace("\n", "<br/>")

    elements.append(Paragraph(clean_data, normal_style))

    doc.build(elements)

    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="cover_letter.pdf"'

    return response