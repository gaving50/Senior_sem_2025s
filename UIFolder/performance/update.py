import time
from display import display_resource_usage
from get_stuff_and_things import get_resource_usage
from get_stuff_and_things import get_process_resource_usage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import sys

# Initialize lists to store the data
cpu_usage_data = []
memory_usage_data = []
disk_usage_data = []
time_data = []

app = QApplication(sys.argv)

timer = None  # Global timer reference
canvas = None  # Reference to the matplotlib canvas

def update(ax):
    cpu_usage, memory_usage, disk_usage = get_resource_usage()
    display_resource_usage(cpu_usage, memory_usage, disk_usage, 100.0, 
                           cpu_usage_data, memory_usage_data, disk_usage_data, time_data, ax)
    
    global canvas
    if canvas:
        canvas.draw()
        canvas.flush_events()  # Ensure UI updates

def do_update(startValue: bool, ax, figure_canvas=None):
    global timer, canvas
    
    # Store the canvas reference
    canvas = figure_canvas
    
    if startValue:
        # Stop any existing timer first
        if timer is not None:
            timer.stop()
        
        # Start a new timer
        timer = QTimer()
        timer.timeout.connect(lambda: update(ax))
        timer.start(500)  # Update every 500 milliseconds
    else:
        # Stop the timer if running
        if timer is not None:
            timer.stop()
            timer = None