import time
import GPUtil
from display import display_resource_usage
from get_stuff_and_things import get_resource_usage
from get_stuff_and_things import get_process_resource_usage
from testUI import MainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import sys

# Initialize lists to store the data
cpu_usage_data = []
memory_usage_data = []
disk_usage_data = []
time_data = []

app = QApplication(sys.argv)
window = MainWindow()
window.show()

def update():
    cpu_usage, memory_usage, disk_usage = get_resource_usage()
    display_resource_usage(cpu_usage, memory_usage, disk_usage, 100.0, cpu_usage_data, memory_usage_data, disk_usage_data, time_data, window.ax)
    # GPUtil.showUtilization()
    window.canvas.draw()

# Set up a QTimer to call the update function periodically
timer = QTimer()
timer.timeout.connect(update)
timer.start(500)  # Update every 500 milliseconds

sys.exit(app.exec())


