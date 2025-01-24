from django.shortcuts import render

import app.src.stats as stats
import app.src.rankings as rankings

def table_view(request):
    table = stats.get_table()

    return render(request, "app/table.html", {"table": table})


def athlete_view(request, name):
    athlete = stats.get_athlete(name)
    pr = stats.get_pr_ipfgl(athlete)
    prs = stats.get_everyone_prs()

    freq, avg_chunk, block = stats.get_distribution_ipfgl(prs=prs)
    pr_chunk = block * round(pr / block)

    percentile = stats.get_percentile(athlete, pr, prs)
    best_lift = stats.get_best_worst_lift(name)

    res = {
        "athlete_comps": athlete,
        "best_lift": best_lift[0],
        "worst_lift": best_lift[1],
        "percentile": percentile,
        "freq_keys": list(freq.keys()),
        "freq_values": list(freq.values()),
        "freq_avg": avg_chunk,
        "freq_pr": pr_chunk,
    }

    return render(request, "app/athlete.html", res)


def rankings_view(request):
    age_class = request.GET.get('age_class', None)
    weight_class = request.GET.get('weight_class', None)
    event = request.GET.get('event_type', None)

    filters = {
        "Division": age_class,
        "WeightClassKg": weight_class,
        "Event": event,
    }

    filters = {key: value for key, value in filters.items() if value}


    r = rankings.get_ranking(filters)


    return render(request, "app/rankings.html", {"ranking": r})