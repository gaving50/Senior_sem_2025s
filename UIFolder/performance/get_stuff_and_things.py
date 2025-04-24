
import psutil




# gets resource usage of the system
# returns cpu usage, memory usage, disk usage
def get_resource_usage():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return cpu_usage, memory_usage, disk_usage





# gets the pid of a specified external process
# process_name: name of the process
def get_process_pid(process_name):
    for process in psutil.process_iter():
        if process.name() == process_name:
            return process.pid
        


# gets the resource usage of a specified external process
# process_name: name of the process
def get_process_resource_usage(process_name):
    pid = get_process_pid(process_name)
    process = psutil.Process(pid)
    return process.cpu_percent(), process.memory_percent()