from scripts.populate_db import populate
from background_task import background


@background(schedule=1)
def populate_db_background_task():
    populate()
