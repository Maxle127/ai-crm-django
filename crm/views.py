from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Lead, Note
from django.contrib.auth.decorators import login_required
from .forms import LeadForm


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
        delete_note_id = request.POST.get("delete_note_id")
        if delete_note_id:
            note = get_object_or_404(Note, id=delete_note_id, lead=lead)
            note.delete()
        else:
            note_text = request.POST.get("note_text")
            if note_text:
                Note.objects.create(note_text=note_text, lead=lead)
            return redirect("lead-detail", id=lead.id)
    return render(request, "crm/lead-detail.html", {"lead": lead})

@login_required
def create_lead(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.owner = request.user
            lead.save()
            return redirect("leads")
    else:
        form = LeadForm()
    return render(request, "crm/create_lead.html", {"form": form})


@login_required
def update_lead(request, id):
    lead = get_object_or_404(Lead, id=id, owner=request.user)
    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            updated_lead = form.save(commit=False)
            updated_lead.owner = request.user
            updated_lead.save()
            return redirect("lead-detail", id=lead.id)
    else:
        form = LeadForm(instance=lead)
    return render(request, "crm/update_lead.html", {"form": form, "lead": lead})


@login_required
def delete_lead(request, id):
    lead = get_object_or_404(Lead, id=id, owner=request.user)
    if request.method == "POST":
        lead.delete()
        return redirect("leads")
    else:
        return render(request, "crm/delete_lead.html", {"lead": lead})