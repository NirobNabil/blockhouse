from background_task import background
import os

@background(schedule=10)
def add_to_del_queue(path):
    print("came to delete")
    os.remove(path)