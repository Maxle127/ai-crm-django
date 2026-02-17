from django.shortcuts import render

async def dashbord(request):
    return render(request, "crm/index.html")

async def leads(request):
    return render(request, "crm/leads.html")

async def lead_detail(request, id):
    return render(request, "crm/lead-detail.html")
 