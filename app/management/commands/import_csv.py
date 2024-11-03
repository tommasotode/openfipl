import os
import pandas as pd

from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Competition


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


class Command(BaseCommand):
    help = "Download and import the CSV dataset in the SQLite database"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path of the CSV file")

    def handle(self, *args, **options):
        path = options["csv_file"]

        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f"Cannot open '{path}'"))
            return

        self.stdout.write(self.style.NOTICE(f"Importing {path} to db.sqlite3"))

        df = pd.read_csv(path)
        instances = [
            Competition(
                Name=row["Name"],
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
            for _, row in df.iterrows()
        ]

        try:
            with transaction.atomic():
                Competition.objects.bulk_create(instances, batch_size=1000)
            self.stdout.write(self.style.SUCCESS("Finished :-)"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
