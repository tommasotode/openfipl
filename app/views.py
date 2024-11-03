from app.models import Competition
from django.shortcuts import render
from django.db.models import Max

from collections import Counter


def display_table(request):
    table = Competition.objects.filter(Federation="IPF").values(
        "Name", "Sex", "TotalKg", "Date"
    )[:1000]

    return render(request, "app/table.html", {"table": table})


def athlete_view(request, name):
    athlete = Competition.objects.filter(Name=name)

    return render(request, "app/athlete.html", {"athlete": athlete})


def distribution(request):
    grouped_best = (
        Competition.objects.filter(Event="SBD")
        .values("Name")
        .annotate(best_total=Max("TotalKg"))
    )

    best = [entry["best_total"] for entry in grouped_best if entry["best_total"] > 0]
    best.sort()
    total_frequency = Counter(best)

    total = list(total_frequency.keys())
    freq = list(total_frequency.values())

    plot = {"total": total, "frequency": freq}

    return render(request, "app/distribution.html", plot)
