from django.http import Http404
from django.shortcuts import render
from datetime import datetime
from .models import Lead

def get_date(lead):
    return lead["created_at"]

def dashbord(request):
    total = Lead.objects.count()
    new_count = Lead.objects.filter(status="New").count()
    contacted_count = Lead.objects.filter(status="Contacted").count()
    won_count = Lead.objects.filter(status="Won").count()

    latest_leads = Lead.objects.order_by("-created_at")[:3]

    context = {
        "total": total,
        "new_count": new_count,
        "contacted_count": contacted_count,
        "won_count": won_count,
        "leads": latest_leads,
    }
    return render(request, "crm/index.html", context)

def leads(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "crm/leads.html", context)

def lead_detail(request, id):
    lead = Lead.objects.get(id=id)
    if lead == None:
        raise Http404()
    return render(request, "crm/lead-detail.html", {"lead": lead})
 