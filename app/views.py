from app.models import Competition
from django.shortcuts import render
from django.db.models import Max

from collections import Counter
from bisect import bisect_left


def get_best_lift(name):
    prs = Competition.objects.filter(Name=name, Event="SBD", Equipment="Raw").aggregate(
        s=Max("BestSquatKg"), b=Max("BestBenchKg"), d=Max("BestDeadliftKg")
    )

    squat = list(
        Competition.objects.filter(Event="SBD", Equipment="Raw")
        .order_by("BestSquatKg")
        .values_list("BestSquatKg", flat=True)
    )

    bench = list(
        Competition.objects.filter(Event="SBD", Equipment="Raw")
        .order_by("-BestBenchKg")
        .values_list("BestBenchKg", flat=True)
    )

    deadlift = list(
        Competition.objects.filter(Event="SBD", Equipment="Raw")
        .order_by("BestDeadliftKg")
        .values_list("BestDeadliftKg", flat=True)
    )

    srank = len(squat) - bisect_left(squat, prs["s"])
    brank = len(bench) - bisect_left(bench, prs["b"])
    drank = len(deadlift) - bisect_left(deadlift, prs["d"])

    high = {
        (srank / len(squat)): "squat",
        (brank / len(bench)): "bench",
        (drank / len(deadlift)): "deadlift",
    }

    best = high[min(high.keys())]
    worst = high[max(high.keys())]

    return (best, worst)


def table_view(request):
    table = (
        Competition.objects.filter(Event="SBD", Equipment="Raw", Federation="FIPL")
        .values("Name", "Sex", "TotalKg", "IPFGLPoints", "Date")
        .order_by("IPFGLPoints")
        .reverse()
    )[:2000]

    return render(request, "app/table.html", {"table": table})


def athlete_view(request, name):
    block = 1

    athlete = Competition.objects.filter(Name=name, Event="SBD", Equipment="Raw")
    pr = athlete.aggregate(m=Max("IPFGLPoints"))["m"]
    prs = (
        Competition.objects.filter(Event="SBD", Equipment="Raw")
        .values("Name")
        .annotate(best=Max("IPFGLPoints"))
    )
    squat = list(
        Competition.objects.filter(Event="SBD", Equipment="Raw")
        .order_by("BestSquatKg")
        .values_list("BestSquatKg", flat=True)
    )

    best = sorted(p["best"] for p in prs if p["best"] > 0)
    freq = Counter(block * (p // block) for p in best)

    avg = sum(best) / len(best) if best else 0
    avg_chunk = block * round(avg / block)
    pr_chunk = block * round(pr / block)

    high = sum(1 for p in best if pr < p)
    percentile = (high / len(best)) * 100

    best_lift = ("deadlift", "bench")
    best_lift = get_best_lift(name)

    res = {
        "athlete": athlete,
        "best": best_lift[0],
        "worst": best_lift[1],
        "percentile": percentile,
        "dist_points": list(freq.keys()),
        "dist_freq": list(freq.values()),
        "dist_avg": avg_chunk,
        "dist_pr": pr_chunk,
    }

    return render(request, "app/athlete.html", res)
