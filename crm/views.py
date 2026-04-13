from django.urls import reverse_lazy
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from datetime import date
import json

from .models import Lead, Note, Profile
from .forms import LeadForm, ProfileForm, RegisterForm
from .ai_service import generate_follow_up


class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = "crm/create_lead.html"
    success_url = reverse_lazy("leads")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class LeadUpdateView(UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = "crm/update_lead.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("lead-detail", kwargs={"id": self.object.id})
    

class LeadDeleteView(DeleteView):
    model = Lead
    template_name = "crm/delete_lead.html"
    success_url = reverse_lazy("leads")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})
    
 
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
    if request.method == "POST":
        status_filter = request.POST.get("status_filter")
        request.session["status_filter"] = status_filter
    else:
        status_filter = request.session.get("status_filter", "all")
    leads = Lead.objects.filter(owner=request.user)
    if status_filter != "all":
        leads = leads.filter(status=status_filter)
    context = {
        "leads": leads,
        "status_filter": status_filter
    }
    return render(request, "crm/leads.html", context)


@login_required
def lead_detail(request, id):
    lead = get_object_or_404(Lead, id=id, owner=request.user)
    follow_up_message = None

    if request.method == "POST":
        delete_note_id = request.POST.get("delete_note_id")
        generate_follow_up_action = request.POST.get("generate_follow_up")

        if delete_note_id:
            note = get_object_or_404(Note, id=delete_note_id, lead=lead)
            note.delete()
            
        elif generate_follow_up_action:    
            notes_text=""
            for note in lead.notes.all():
                notes_text += note.note_text +"\n"
            follow_up_message = generate_follow_up(lead.first_name, lead.status, lead.source, notes_text)

        else:
            note_text = request.POST.get("note_text")

            if note_text:
                Note.objects.create(note_text=note_text, lead=lead)

            return redirect("lead-detail", id=lead.id)
        
    return render(request, "crm/lead-detail.html", {"lead": lead, "follow_up_message": follow_up_message})


def home(request):
    return render(request, "crm/home.html" )


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            return redirect("profile")
        
    else:
        form = ProfileForm(instance=profile)
        
    my_leads = Lead.objects.filter(owner=request.user)

    total = my_leads.count()
    new_count = my_leads.filter(status="new").count()
    contacted_count = my_leads.filter(status="contacted").count()
    won_count = my_leads.filter(status="won").count()
    lost_count = my_leads.filter(status="lost").count()
    
    today = date.today()
    current_month = today.month
    current_year = today.year
    
    monthly_leads = my_leads.filter(
        created_at__year=current_year,
        created_at__month=current_month
    )
    labels = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"]
    
    new_chart = [0, 0, 0, 0, 0]
    contacted_chart = [0, 0, 0, 0, 0]
    won_chart = [0, 0, 0, 0, 0]
    lost_chart = [0, 0, 0, 0, 0]
    
    for lead in monthly_leads:
        day = lead.created_at.day
        week_index = (day - 1) //  7
        
        if lead.status == "new":
            new_chart[week_index] += 1
        if lead.status == "contacted":
            contacted_chart[week_index] += 1
        if lead.status == "won":
            won_chart[week_index] += 1
        if lead.status == "lost":
            lost_chart[week_index] += 1
    
    context = {
        "profile": profile,
        "form": form,
        "total_leads": total,
        "new_leads": new_count,
        "contacted_leads": contacted_count,
        "won_leads": won_count,
        "lost_leads": lost_count,
        "chart_labels": json.dumps(labels),
        "new_chart": json.dumps(new_chart),
        "contacted_chart": json.dumps(contacted_chart),
        "won_chart": json.dumps(won_chart),
        "lost_chart": json.dumps(lost_chart),
    }
    
    
    return render(request, "crm/profile.html", context)


