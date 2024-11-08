import os
import pandas as pd

from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Competition

import requests
import zipfile
from tqdm import tqdm


# TODO: Make parser for each field
def get_float(field):
    res = field
    try:
        res = float(field)
    except:
        res = 0.0

    if pd.isna(res) or res is None:
        return 0.0
    else:
        return res


def get_int(field):
    res = field
    try:
        res = int(field)
    except:
        res = 0

    if pd.isna(res) or res is None:
        return 0
    else:
        return res


def get_name(name):
    res = name.replace("#", "")

    return res


class Command(BaseCommand):
    def download_csv(self, url: str, directory: str) -> str:
        tmp_path = "temp.zip"

        self.stdout.write(self.style.NOTICE("Downloading dataset..."))
        res = requests.get(url)
        res.raise_for_status()
        with open(tmp_path, "wb") as file:
            file.write(res.content)

        print("Extracting dataset...")
        os.makedirs(directory, exist_ok=True)
        with zipfile.ZipFile(tmp_path, "r") as z:
            z.extractall(directory)

        os.remove(tmp_path)
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".csv"):
                    old = os.path.join(root, file)
                    new = os.path.join(directory, "dataset.csv")
                    os.replace(old, new)

        return new

    def handle(self, *args, **options):
        path = self.download_csv(
            "https://openpowerlifting.gitlab.io/opl-csv/files/openipf-latest.zip",
            "dataset",
        )

        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f"Cannot open '{path}'"))
            return

        self.stdout.write(self.style.NOTICE("Reading dataset..."))
        df = pd.read_csv(path)
        instances = [
            Competition(
                Name=get_name(row["Name"]),
                Sex=row["Sex"],
                Event=row["Event"],
                Equipment=row["Equipment"],
                Age=get_int(row["Age"]),
                Division=row["Division"],
                BodyweightKg=get_float(row["BodyweightKg"]),
                WeightClassKg=row["WeightClassKg"],
                BestSquatKg=get_float(row["Best3SquatKg"]),
                BestBenchKg=get_float(row["Best3BenchKg"]),
                BestDeadliftKg=get_float(row["Best3DeadliftKg"]),
                TotalKg=get_float(row["TotalKg"]),
                Place=get_int(row["Place"]),
                IPFGLPoints=get_float(row["Goodlift"]),
                Country=row["Country"],
                Federation=row["Federation"],
                Date=row["Date"],
                MeetName=row["MeetName"],
            )
            for _, row in tqdm(df.iterrows())
        ]

        self.stdout.write(self.style.NOTICE("Importing dataset to db.sqlite3..."))
        try:
            Competition.objects.all().delete()
            with transaction.atomic():
                Competition.objects.bulk_create(instances, batch_size=1000)
            self.stdout.write(self.style.SUCCESS("Finished :-)"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
