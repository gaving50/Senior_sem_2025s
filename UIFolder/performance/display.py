import time
import matplotlib.pyplot as plt

# displays resource usage of the system as bars and percents
# cpu_usage: cpu usage percentage
# memory_usage: memory usage percentage
# disk_usage: disk usage percentage
# bars: number of bars to display
def display_resource_usage(cpu_usage, memory_usage, gpu_usage, bars, cpu_usage_data, memory_usage_data, gpu_usage_data, time_data, ax):
    cpu_percentage = cpu_usage / 100.0
    memory_percentage = memory_usage / 100.0
    gpu_percentage = gpu_usage / 100.0
    # cpu_bar = '█' * int(cpu_percentage * bars) + '-' * int(bars - cpu_percentage * bars)
    # memory_bar = '█' * int(memory_percentage * bars) + '-' * int(bars - memory_percentage * bars)
    # disk_bar = '█' * int(disk_percentage * bars) + '-' * int(bars - disk_percentage * bars)
    # print(f'CPU Usage: {cpu_usage}% \n |{cpu_bar}|')
    # print(f'Memory Usage: {memory_usage}% \n |{memory_bar}|')
    # print(f'Disk Usage: {disk_usage}% \n |{disk_bar}|')

    # # Append the data
    # cpu_usage_data.append(cpu_usage)
    # memory_usage_data.append(memory_usage)
    # gpu_usage_data.append(gpu_usage)
    # time_data.append(time.time())

    # # Limit the data to the last 10 seconds
    # if len(cpu_usage_data) > 20:
    #     cpu_usage_data.pop(0)
    #     memory_usage_data.pop(0)
    #     gpu_usage_data.pop(0)
    #     time_data.pop(0)

    # Update the plots
    ax[0].cla()
    ax[1].cla()
    ax[2].cla()

    ax[0].plot(time_data, cpu_usage_data, label='CPU Usage')
    ax[1].plot(time_data, memory_usage_data, label='Memory Usage')
    ax[2].plot(time_data, gpu_usage_data, label='GPU Usage')

    ax[0].set_ylabel('CPU Usage (%)')
    ax[1].set_ylabel('Memory Usage (%)')
    ax[2].set_ylabel('GPU Usage (%)')
    ax[2].set_xlabel('Time (s)')

    ax[0].legend()
    ax[1].legend()
    ax[2].legend()

    #Adjusts bottom of graph to fit better
    plt.subplots_adjust(bottom=0.2)  
    
    plt.tight_layout(pad=3.0)  
