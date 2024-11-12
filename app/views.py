from app.models import Competition
from django.shortcuts import render
from django.db.models import Max

from collections import Counter
from bisect import bisect_left

def get_best_lift(name):
    pr = (
        Competition.objects.filter(Name=name, Event="SBD", Equipment="Raw")
        .aggregate(s=Max("BestSquatKg"), b=Max("BestBenchKg"), d=Max("BestDeadliftKg"))
    )
    prs = (
        Competition.objects.filter(Event="SBD", Equipment="Raw")
        .values("Name")
        .annotate(s=Max("BestSquatKg"), b=Max("BestBenchKg"), d=Max("BestDeadliftKg"))
    )
    squat = sorted(p['s'] for p in prs if p['s'] >= 20)
    bench = sorted(p['b'] for p in prs if p['b'] >= 20)
    deadlift = sorted(p['d'] for p in prs if p['d'] >= 20)

    srank = len(squat) - bisect_left(squat, pr['s'])
    brank = len(bench) - bisect_left(bench, pr['b'])
    drank = len(deadlift) - bisect_left(deadlift, pr['d'])

    high = {
        (srank / len(squat)): "squat",
        (brank / len(bench)): "bench",
        (drank / len(deadlift)): "deadlift"
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
    best = sorted([p["best"] for p in prs if p["best"] > 0])
    freq = Counter([block * (p // block) for p in best])

    avg = sum(best) / len(best) if best else 0
    avg_chunk = block * round(avg / block)
    pr_chunk = block * round(pr / block)

    high = sum(1 for p in best if pr < p)
    percentile = (high / len(best)) * 100

    best_lift = get_best_lift(name)

    res = {
        "athlete": athlete,
        "best" : best_lift[0],
        "worst" : best_lift[1],
        "percentile": percentile,
        "dist_points": list(freq.keys()),
        "dist_freq": list(freq.values()),
        "dist_avg": avg_chunk,
        "dist_pr": pr_chunk,
    }

    return render(request, "app/athlete.html", res)
