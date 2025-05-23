import time
from .display import display_resource_usage
from .get_stuff_and_things import get_resource_usage
from .get_stuff_and_things import get_ollama_resource_usage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import sys

# Initialize lists to store the data
cpu_usage_data = []
memory_usage_data = []
gpu_usage_data = []  # Renamed from disk_usage_data
time_data = []

app = QApplication(sys.argv)

timer = None  # Global timer reference
canvas = None  # Reference to the matplotlib canvas
data_limit = 60  # Number of data points to keep

def update(ax):
    # Get resource usage for the ollama process
    cpu_usage, memory_usage, gpu_usage = get_ollama_resource_usage()

    # Append the data to the respective lists
    cpu_usage_data.append(cpu_usage)
    memory_usage_data.append(memory_usage)
    gpu_usage_data.append(gpu_usage)  # Append GPU usage
    time_data.append(time.time())

    # Limit the data to the last data_limit/2 seconds
    if len(cpu_usage_data) > data_limit:
        cpu_usage_data.pop(0)
        memory_usage_data.pop(0)
        gpu_usage_data.pop(0)
        time_data.pop(0)

    # Update the graph
    display_resource_usage(cpu_usage, memory_usage, gpu_usage, 100.0, 
                           cpu_usage_data, memory_usage_data, gpu_usage_data, time_data, ax)
    
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