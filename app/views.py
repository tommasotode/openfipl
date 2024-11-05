from app.models import Competition
from django.shortcuts import render
from django.db.models import Max

from collections import Counter


def display_table(request):
    table = (
        Competition.objects.filter(Event="SBD")
        .filter(Federation="FIPL")
        .filter(Equipment="Raw")
        .values("Name", "Sex", "TotalKg", "Date")[2000:3000]
    )

    return render(request, "app/table.html", {"table": table})


def athlete_view(request, name):
    athlete = (
        Competition.objects.filter(Name=name)
        .filter(Event="SBD")
        .filter(Equipment="Raw")
    )
    pr = athlete.aggregate(max_points=Max("IPFGLPoints"))["max_points"]

    prs = (
        Competition.objects.filter(Event="SBD")
        .filter(Equipment="Raw")
        .filter(Sex="M")
        .values("Name")
        .annotate(best_total=Max("IPFGLPoints"))
    )
    best = [entry["best_total"] for entry in prs if entry["best_total"] > 0]
    best.sort()

    chunk = 1
    best_chunks = [chunk * (total // chunk) for total in best]
    freq = Counter(best_chunks)
    total = list(freq.keys())
    freq = list(freq.values())
    avg = sum(best) / len(best) if best else 0
    avg_chunk = chunk * round(avg / chunk)
    pr_chunk = chunk * round(pr / chunk)

    res = {
        "athlete": athlete,
        "dist_total": total,
        "dist_frequency": freq,
        "dist_average": avg_chunk,
        "dist_pr": pr_chunk,
    }

    return render(request, "app/athlete.html", res)


def distribution(request):
    athlete_best = (
        Competition.objects.filter(Event="SBD")
        .filter(Equipment="Raw")
        .filter(Sex="M")
        .values("Name")
        .annotate(best_total=Max("IPFGLPoints"))
    )
    best = [entry["best_total"] for entry in athlete_best if entry["best_total"] > 0]
    best.sort()

    chunk = 1

    best_chunks = [chunk * (total // chunk) for total in best]
    freq = Counter(best_chunks)
    total = list(freq.keys())
    freq = list(freq.values())

    avg = sum(best) / len(best) if best else 0
    avg_chunk = chunk * round(avg / chunk)

    res = 80
    res_chunk = chunk * round(res / chunk)

    plot = {
        "total": total,
        "frequency": freq,
        "average": avg_chunk,
        "result": res_chunk,
    }

    return render(request, "app/distribution.html", plot)
