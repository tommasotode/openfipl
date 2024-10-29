from django.shortcuts import render

import pandas as pd


def display_table(request):

    df = pd.read_csv("openipf-2024-10-26/openipf-2024-10-26-469a3a20.csv")
    df = df[100:200]
    html_table = df.to_html(index=False)

    return render(request, "app/table.html", {"table": html_table})
