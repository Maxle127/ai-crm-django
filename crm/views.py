from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Lead, Note
from django.contrib.auth.decorators import login_required

@login_required
def dashbord(request):
    my_leads = Lead.objects.filter(owner=request.user)
    total = my_leads.count()
    new_count = my_leads.filter(status="new").count()
    contacted_count = my_leads.filter(status="contacted").count()
    won_count = my_leads.filter(status="won").count()

    latest_leads = my_leads.order_by("-updated_at")[:3]

    context = {
        "total": total,
        "new_count": new_count,
        "contacted_count": contacted_count,
        "won_count": won_count,
        "leads": latest_leads,
    }
    return render(request, "crm/index.html", context)

@login_required
def leads(request):
    leads = Lead.objects.filter(owner=request.user)
    context = {
        "leads": leads
    }
    return render(request, "crm/leads.html", context)

@login_required
def lead_detail(request, id):
    lead = get_object_or_404(Lead, id=id, owner=request.user)
    if lead == None:
        raise Http404()
    if request.method == "POST":
        note_text = request.POST.get("note_text")
        if note_text:
            Note.objects.create(note_text=note_text, lead=lead)
        return redirect("lead-detail", id=lead.id)
    return render(request, "crm/lead-detail.html", {"lead": lead})

@login_required
def create_lead(request):
    if request.method == "POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email = request.POST.get("email")
        phone=request.POST.get("phone")
        Lead.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone, owner=request.user)
        return redirect("leads")
    return render(request, "crm/create_lead.html")
