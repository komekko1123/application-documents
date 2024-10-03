import pandas as pd
import matplotlib.pyplot as plt

# 資料
waiting_time_data = {
    "ID": [1, 2, 3, 4, 5, 6],
    "FCFS": [0, 0, 20, 15, 0, 5],
    "RR": [0, 20, 30, 15, 0, 5],
    "SJF": [0, 0, 20, 15, 0, 5],
    "SRTF": [0, 0, 20, 15, 0, 5],
    "HRRN": [0, 0, 20, 15, 0, 5],
    "PPRR": [0, 30, 35, 0, 10, 0]
}

# 轉換成DataFrame
waiting_time_df = pd.DataFrame(waiting_time_data)

# 計算每种算法的平均等待时间
average_waiting_time = waiting_time_df.mean()
# 繪製直方圖
average_waiting_time.drop("ID").plot(kind='bar', alpha=0.7)
plt.title("Average Waiting Time per CPU Scheduler(out_input3)")
plt.xlabel("CPU Schedule")
plt.ylabel("Average Waiting Time")
plt.grid(True)
plt.show()


turnaround_time_data = {
    "ID": [1, 2, 3, 4, 5, 6],
    "FCFS": [20, 25, 45, 30, 10, 15],
    "RR": [20, 45, 55, 30, 10, 15],
    "SJF": [20, 25, 45, 30, 10, 15],
    "SRTF": [20, 25, 45, 30, 10, 15],
    "HRRN": [20, 25, 45, 30, 10, 15],
    "PPRR": [20, 55, 60, 15, 20, 10]
}

# 转换成DataFrame
turnaround_time_df = pd.DataFrame(turnaround_time_data)

# 绘制箱型图
turnaround_time_df.drop(columns=["ID"]).boxplot()
plt.title("Turnaround Time Boxplot(out_input3)")
plt.ylabel("Time")
plt.xlabel("CPU Schedule")
plt.xticks(rotation=45)
plt.show()