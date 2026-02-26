
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import ToolUsage
from html2image import Html2Image
import tempfile
import os


@login_required
def tools(request):
    return render(request, "dashboard/tools.html")

@login_required
def webpage_to_image(request):

    if request.method == "POST":
        url = request.POST.get("url")

        hti = Html2Image()
        hti.output_path = tempfile.gettempdir()

        paths = hti.screenshot(url=url, save_as="page.png")
        file_path = paths[0]   # ⭐ SAFE

        ToolUsage.objects.create(user=request.user, tool="image", url=url)

        with open(file_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")

    return render(request, "dashboard/tools.html")


@login_required
def webpage_screenshot(request):

    if request.method == "POST":
        url = request.POST.get("url")

        hti = Html2Image()
        hti.output_path = tempfile.gettempdir()

        paths = hti.screenshot(url=url, save_as="shot.png")
        file_path = paths[0]

        ToolUsage.objects.create(user=request.user, tool="screenshot", url=url)

        with open(file_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")

    return render(request, "dashboard/tools.html")
        



from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib.pagesizes import letter

@login_required
def webpage_to_pdf(request):

    if request.method == "POST":
        url = request.POST.get("url")

        hti = Html2Image()

        temp = tempfile.gettempdir()
        hti.output_path = temp

        img_name = "temp.png"
        img_path = os.path.join(temp, img_name)

        # ⭐ screenshot
        hti.screenshot(url=url, save_as=img_name)

        # ⭐ create pdf
        pdf_path = os.path.join(temp, "page.pdf")

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)

        # ⭐ IMPORTANT — AUTO SCALE
        img = Image(img_path)
        img.drawWidth = 450   # safe width
        img.drawHeight = img.drawHeight * (450 / img.drawWidth)

        story = [img]
        doc.build(story)

        ToolUsage.objects.create(user=request.user, tool="pdf", url=url)

        with open(pdf_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="page.pdf"'
            return response