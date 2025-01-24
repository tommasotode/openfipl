from app.models import Performance

from app.utils import benchmark

filters = {"Event": "SBD", "Equipment": "Raw"}

@benchmark
def get_ranking(top=10, filters=None):
    table = (
        Performance.objects.filter(Event="SBD", Equipment="Raw", Federation="FIPL")
        .values("Name", "Sex", "TotalKg", "IPFGLPoints", "Date")
        .order_by("IPFGLPoints")
        .reverse()
    )[:top]

    return table