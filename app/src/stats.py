from app.models import Performance
from django.db.models import Max

from collections import Counter
from bisect import bisect_right

from app.utils import benchmark


# TODO: Use in all queries, based on user choice:
filters = {"Event": "SBD", "Equipment": "Raw"}


@benchmark
def get_table(rows=1000):
    table = (
        Performance.objects.filter(Event="SBD", Equipment="Raw", Federation="FIPL")
        .values("Name", "Sex", "TotalKg", "IPFGLPoints", "Date")
        .order_by("IPFGLPoints")
        .reverse()
    )[:rows]

    return table


# TODO: maybe it's better to sort from the db,
# but testing it says the opposite, why?
@benchmark
def get_everyone_prs(nonzero=True):
    prs = (
        Performance.objects.filter(Event="SBD", Equipment="Raw")
        .values("Name")
        .annotate(best=Max("IPFGLPoints"))
    )
    if nonzero:
        best = sorted(p["best"] for p in prs if p["best"] > 0)
    else:
        best = sorted(p["best"] for p in prs)

    return best


@benchmark
def get_distribution_ipfgl(block=1, based_on_prs=True, prs=None):
    if based_on_prs:
        if not prs:
            best = get_everyone_prs()
        else:
            best = prs
    else:
        points = Performance.objects.filter(Event="SBD", Equipment="Raw").values_list(
            "IPFGLPoints"
        )
        best = sorted(p for p in points if p > 0)

    avg = sum(best) / len(best) if best else 0
    freq = Counter(block * (p // block) for p in best)
    avg_chunk = block * round(avg / block)

    return (freq, avg_chunk, block)


@benchmark
def get_athlete(name):
    athlete = Performance.objects.filter(
        Name=name, Event="SBD", Equipment="Raw"
    ).order_by("Date")
    return athlete


@benchmark
def get_pr_ipfgl(athlete):
    pr = max(athlete.values_list("IPFGLPoints", flat=True))
    return pr


@benchmark
def get_pr_total(athlete):
    pr = max(athlete.values_list("TotalKg", flat=True))
    return pr


@benchmark
def get_pr_squat(athlete):
    pr = max(athlete.values_list("BestSquatKg", flat=True))
    return pr


@benchmark
def get_pr_bench(athlete):
    pr = max(athlete.values_list("BestBenchKg", flat=True))
    return pr


@benchmark
def get_pr_deadlift(athlete):
    pr = max(athlete.values_list("BestDeadliftKg", flat=True))
    return pr


@benchmark
def get_best_worst_lift(athlete):
    best = "fix"
    worst = "fix"

    return (best, worst)


@benchmark
def get_percentile(athlete, pr=None, prs=None):
    if not pr:
        pr = get_pr_ipfgl(athlete)
    if not prs:
        prs = get_everyone_prs()

    rank = len(prs) - bisect_right(prs, pr)
    percentile = 100 - (
        (rank / len(prs) if prs else -1) * 100
    )  # better than x% of athletes

    return percentile
