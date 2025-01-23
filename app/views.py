from django.shortcuts import render

import src.stats as stats


def table_view(request):
    table = stats.get_table()

    return render(request, "app/table.html", {"table": table})


def athlete_view(request, name):
    freq, avg_chunk, block = stats.get_ipfgl_distribution()

    athlete = stats.get_athlete(name)

    pr = stats.get_pr(athlete)
    pr_chunk = block * round(pr / block)

    best_lift = stats.get_best_lift(name)

    res = {
        "athlete": athlete,
        "best": best_lift[0],
        "worst": best_lift[1],
        "percentile": -1,
        "dist_points": list(freq.keys()),
        "dist_freq": list(freq.values()),
        "dist_avg": avg_chunk,
        "dist_pr": pr_chunk,
    }

    return render(request, "app/athlete.html", res)
