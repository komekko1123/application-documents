import pandas as pd
import matplotlib.pyplot as plt

# 資料
waiting_time_data = {
    "ID": [1, 2, 3, 4],
    "FCFS": [0, 4, 4, 7],
    "RR": [5, 2, 8, 7],
    "SJF": [0, 4, 9, 1],
    "SRTF": [3, 0, 9, 1],
    "HRRN": [0, 4, 4, 7],
    "PPRR": [9, 0, 9, 0]
}

# 轉換成DataFrame
waiting_time_df = pd.DataFrame(waiting_time_data)

# 計算每种算法的平均等待时间
average_waiting_time = waiting_time_df.mean()
# 繪製直方圖
average_waiting_time.drop("ID").plot(kind='bar', alpha=0.7)
plt.title("Average Waiting Time per CPU Scheduler(out_input4)")
plt.xlabel("CPU Schedule")
plt.ylabel("Average Waiting Time")
plt.grid(True)
plt.show()


turnaround_time_data = {
    "ID": [1, 2, 3, 4],
    "FCFS": [6, 7, 10, 12],
    "RR": [11, 5, 14, 12],
    "SJF": [6, 7, 15, 6],
    "SRTF": [9, 3, 15, 6],
    "HRRN": [6, 7, 10, 12],
    "PPRR": [15, 3, 15, 5]
}

# 转换成DataFrame
turnaround_time_df = pd.DataFrame(turnaround_time_data)

# 绘制箱型图
turnaround_time_df.drop(columns=["ID"]).boxplot()
plt.title("Turnaround Time Boxplot(out_input4)")
plt.ylabel("Time")
plt.xlabel("CPU Schedule")
plt.xticks(rotation=45)
plt.show()