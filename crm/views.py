from django.shortcuts import render
from datetime import datetime

LEADS = {
    1 : {
        "first_name": "Maksym",
        "last_name": "Leiza",
        "email": "maksimleiza@gmail.com",
        "phone": "+380 (50) 621-68-97",
        "status": "New",
        "source": "Telegram",
        "created_at": datetime(2026, 2, 18, 1, 30),
    },
    2: {
        "first_name": "Veronika",
        "last_name": "Grinda",
        "email": "veronikagr@gmail.com",
        "phone": "+380 (50) 000-00-00",
        "status": "Contacted",
        "source": "Instagram",
        "created_at": datetime(2026, 2, 17, 2, 30),
    },
    3 : {
        "first_name": "Sasha",
        "last_name": "Bui",
        "email": "sashabui@gmail.com",
        "phone": "+380 (50) 123-45-67",
        "status": "Won",
        "source": "Website",
        "created_at": datetime(2026, 2, 15, 19, 30),
    },

    4 : {
        "first_name": "Zhenya",
        "last_name": "Babinets",
        "email": "zhenchy@gmail.com",
        "phone": "+380 (67) 696-69-69",
        "status": "Won",
        "source": "Website",
        "created_at": datetime(2026, 2, 15, 19, 45),
    },
}

def get_date(lead):
    return lead["created_at"]

async def dashbord(request):
    total = len(LEADS)
    new_count = sum(1 for lead in LEADS.values() if lead["status"] == "New")
    contacted_count = sum(1 for lead in LEADS.values() if lead["status"] == "Contacted")
    won_count = sum(1 for lead in LEADS.values() if lead["status"] == "Won")

    sorted_leads = sorted(LEADS.values(), key=get_date, reverse=True)
    latest_leads = sorted_leads[:3]

    context = {
        "total": total,
        "new_count": new_count,
        "contacted_count": contacted_count,
        "won_count": won_count,
        "leads": latest_leads,
    }
    return render(request, "crm/index.html", context)

async def leads(request):
    context = {
        "leads": LEADS
    }
    return render(request, "crm/leads.html", context)

async def lead_detail(request, id):
    lead = LEADS.get(id)
    return render(request, "crm/lead-detail.html", {"lead": lead})
 