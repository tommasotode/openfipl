from django.shortcuts import render
from app.models import Athletes

def display_table(request):

    table = Athletes.objects.filter(Federation="IPF").values("Name", "Sex", "TotalKg", "Date")[:1000]

    return render(request, "app/table.html", {"table": table})


def athlete_view(request, name):    
    athlete = Athletes.objects.filter(Name=name)

    return render(request, "app/athlete.html", {"athlete": athlete})