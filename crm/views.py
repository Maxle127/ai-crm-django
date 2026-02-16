from django.shortcuts import render

async def dashbord(request):
    return render(request, "crm/index.html")

async def leads(request):
    pass

async def lead_detail(request, id=1):
    pass
 