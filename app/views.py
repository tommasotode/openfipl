from app.models import Competition
from django.shortcuts import render
from django.db.models import Max

from collections import Counter


def display_table(request):
    table = Competition.objects.filter(Event="SBD").filter(Federation="FIPL").values(
        "Name", "Sex", "TotalKg", "Date"
    )[2000:3000]

    return render(request, "app/table.html", {"table": table})


def athlete_view(request, name):
    athlete = Competition.objects.filter(Name=name).filter(Event="SBD")

    return render(request, "app/athlete.html", {"athlete": athlete})


def distribution(request):
    athlete_best = (
        Competition.objects.filter(Event="SBD")
        .filter(Equipment="Raw")
        .filter(Sex="M")
        .values("Name")
        .annotate(best_total=Max("TotalKg"))
    )

    best = [entry["best_total"] for entry in athlete_best if entry["best_total"] > 0]
    best.sort()

    grouped_best = [5 * (total // 5) for total in best]
    total_frequency = Counter(grouped_best)

    total = list(total_frequency.keys())
    freq = list(total_frequency.values())

    plot = {"total": total, "frequency": freq}

    return render(request, "app/distribution.html", plot)
