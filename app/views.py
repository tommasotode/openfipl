from app.models import Competition
from django.shortcuts import render
from django.db.models import Max

from collections import Counter


def display_table(request):
    table = Competition.objects.filter(
        Event="SBD", Equipment="Raw", Federation="FIPL"
    ).values("Name", "Sex", "TotalKg", "Date")[2000:3000]

    return render(request, "app/table.html", {"table": table})


def athlete_view(request, name):
    chunk = 1

    athlete = Competition.objects.filter(Name=name, Event="SBD", Equipment="Raw")
    pr = athlete.aggregate(max_points=Max("IPFGLPoints"))["max_points"]
    
    prs = (
        Competition.objects.filter(Event="SBD", Equipment="Raw")
        .values("Name")
        .annotate(best_total=Max("IPFGLPoints"))
    )
    best = [entry["best_total"] for entry in prs if entry["best_total"] > 0]
    best.sort()

    best_chunks = [chunk * (total // chunk) for total in best]
    freq = Counter(best_chunks)
    avg = sum(best) / len(best) if best else 0
    avg_chunk = chunk * round(avg / chunk)
    pr_chunk = chunk * round(pr / chunk)

    res = {
        "athlete": athlete,
        "dist_total": list(freq.keys()),
        "dist_frequency": list(freq.values()),
        "dist_average": avg_chunk,
        "dist_pr": pr_chunk,
    }

    return render(request, "app/athlete.html", res)