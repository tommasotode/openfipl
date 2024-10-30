import csv
from django.core.management.base import BaseCommand
from app.models import Athletes
from tqdm import tqdm

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        path = 'openipf-2024-10-26/openipf-2024-10-26-469a3a20.csv'

        Athletes.objects.all().delete()
        with open(path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for entry in tqdm(reader):
                
                total = entry["TotalKg"]
                try:
                    total = float(total)
                except:
                    total = 0.0
                
                Athletes.objects.create(
                    Name = entry["Name"],
                    Sex = entry["Sex"],
                    Event = entry["Event"],
                    Equipment = entry["Equipment"],
                    Division = entry["Division"],
                    WeightClassKg = entry["WeightClassKg"],
                    TotalKg = total,
                    Federation = entry["Federation"],
                    Date = entry["Date"],
                    MeetName = entry["MeetName"]
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported CSV data'))