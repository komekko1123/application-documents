import pandas as pd
import matplotlib.pyplot as plt

waiting_time_data = {
    "ID": [1, 2, 3, 4, 5],
    "FCFS": [0, 10, 10, 11, 11],
    "RR": [13, 2, 2, 6, 9],
    "SJF": [0, 10, 12, 8, 11],
    "SRTF": [13, 0, 0, 1, 1],
    "HRRN": [0, 10, 12, 8, 11],
    "PPRR": [0, 21, 8, 9, 9]
}




# 轉換成DataFrame
waiting_time_df = pd.DataFrame(waiting_time_data)

# 計算每种算法的平均等待时间
average_waiting_time = waiting_time_df.mean()
# 繪製直方圖
average_waiting_time.drop("ID").plot(kind='bar', alpha=0.7)
plt.title("Average Waiting Time per CPU Scheduler(out_input2)")
plt.xlabel("CPU Schedule")
plt.ylabel("Average Waiting Time")
plt.grid(True)
plt.show()


turnaround_time_data = {
    "ID": [1, 2, 3, 4, 5],
    "FCFS": [11, 12, 13, 13, 17],
    "RR": [24, 4, 5, 8, 15],
    "SJF": [11, 12, 15, 10, 17],
    "SRTF": [24, 2, 3, 3, 7],
    "HRRN": [11, 12, 15, 10, 17],
    "PPRR": [11, 23, 11, 11, 15]
}

# 转换成DataFrame
turnaround_time_df = pd.DataFrame(turnaround_time_data)

# 绘制箱型图
turnaround_time_df.drop(columns=["ID"]).boxplot()
plt.title("Turnaround Time Boxplot(out_input2)")
plt.ylabel("Time")
plt.xlabel("CPU Schedule")
plt.xticks(rotation=45)
plt.show()
