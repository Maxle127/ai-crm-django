from django.urls import reverse_lazy
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lead, Note
from django.contrib.auth.decorators import login_required
from .forms import LeadForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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
