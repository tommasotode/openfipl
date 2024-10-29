from django.http import HttpResponse
from django.shortcuts import render

import pandas as pd


def display_table(request):
    df = pd.read_csv("openipf-2024-10-26/openipf-2024-10-26-469a3a20.csv")
    df = df[df["Federation"]=="FIPL"]
    df = df[df["Date"]>"2000-0-0"]
    df = df[:100]
    df = df[["Name", "Date", "Sex", "TotalKg"]]

    df['Name'] = df.apply(lambda row: f'<a href="/detail/{row["Name"]}/">{row["Name"]}</a>', axis=1)

    html_table = df.to_html(index=False, escape=False)

    return render(request, "app/table.html", {"table": html_table})


def detail_view(request, name):
    df = pd.read_csv("openipf-2024-10-26/openipf-2024-10-26-469a3a20.csv")

    athlete = df[df["Name"] == name]

    if athlete.empty:
        return HttpResponse("No data found for this entry.")

    athlete = athlete.to_dict(orient="records")

    return render(request, "app/detail.html", {"athlete": athlete})