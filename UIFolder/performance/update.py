import time
import GPUtil
from performance.display import display_resource_usage
from performance.get_stuff_and_things import get_resource_usage
from performance.get_stuff_and_things import get_process_resource_usage
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import sys

# Initialize lists to store the data
cpu_usage_data = []
memory_usage_data = []
disk_usage_data = []
time_data = []

app = QApplication(sys.argv)

timer = None  # Global timer reference

def update(ax):
    cpu_usage, memory_usage, disk_usage = get_resource_usage()
    display_resource_usage(cpu_usage, memory_usage, disk_usage, 100.0, cpu_usage_data, memory_usage_data, disk_usage_data, time_data, ax)

def do_update(startValue: bool, ax):
    global timer
    if startValue:
        # Start the timer if not already running
        if timer is None:
            timer = QTimer()
            timer.timeout.connect(lambda: update(ax))
            timer.start(500)  # Update every 500 milliseconds
    else:
        # Stop the timer if running
        if timer is not None:
            timer.stop()
            timer = None

