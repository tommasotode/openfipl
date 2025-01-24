from app.models import Performance

from app.utils import benchmark



@benchmark
def get_ranking(filters=None, top=10):
    '''
    Sub-Juniors o Sub-Junior
    Juniors o Junior
    Open
    Masters N
    Seniors
    '''
    if filters is None:
        filters = {}
        
    table = (
        Performance.objects.filter(Equipment="Raw", Federation="FIPL", **filters)
        .values("Name", "Sex", "TotalKg", "IPFGLPoints", "Date")
        .order_by("IPFGLPoints")
        .order_by("TotalKg")
        .reverse()
    )[:top]

    return table