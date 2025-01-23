from app.models import Competition
from django.db.models import Max

from collections import Counter
from bisect import bisect_left

from app.utils import benchmark


@benchmark
def get_table(rows=1000):
    table = (
        Competition.objects.filter(Event="SBD", Equipment="Raw", Federation="FIPL")
        .values("Name", "Sex", "TotalKg", "IPFGLPoints", "Date")
        .order_by("IPFGLPoints")
        .reverse()
    )[:rows]

    return table


@benchmark
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


@benchmark
def get_ipfgl_distribution(block=1):
    prs = (
        Competition.objects.filter(Event="SBD", Equipment="Raw")
        .values("Name")
        .annotate(best=Max("IPFGLPoints"))
    )

    best = sorted(p["best"] for p in prs if p["best"] > 0)
    avg = sum(best) / len(best) if best else 0
    
    freq = Counter(block * (p // block) for p in best)
    avg_chunk = block * round(avg / block)

    return (freq, avg_chunk, block)


@benchmark
def get_athlete(name):
    athlete = Competition.objects.filter(Name=name, Event="SBD", Equipment="Raw")
    return athlete


@benchmark
def get_pr(athlete):
    pr = athlete.aggregate(m=Max("IPFGLPoints"))["m"]
    return pr

