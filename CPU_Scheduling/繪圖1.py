import pandas as pd
import matplotlib.pyplot as plt

# 資料
waiting_time_data = {
    "ID": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 20, 27, 29],
    "FCFS": [19, 13, 22, 18, 13, 20, 0, 15, 21, 5, 8, 18, 13, 16, 14],
    "RR": [18, 8, 19, 25, 19, 27, 15, 2, 14, 13, 37, 3, 17, 28, 31],
    "SJF": [5, 5, 2, 6, 7, 19, 5, 2, 0, 0, 49, 4, 5, 9, 15],
    "SRTF": [0, 0, 2, 6, 0, 19, 6, 0, 0, 1, 49, 0, 0, 19, 19],
    "HRRN": [19, 5, 16, 14, 13, 23, 0, 3, 11, 6, 18, 4, 13, 9, 20],
    "PPRR": [0, 0, 14, 0, 11, 21, 11, 55, 9, 0, 45, 0, 40, 10, 4]
}

# 轉換成DataFrame
waiting_time_df = pd.DataFrame(waiting_time_data)

# 計算每种算法的平均等待时间
average_waiting_time = waiting_time_df.mean()
# 繪製直方圖
average_waiting_time.drop("ID").plot(kind='bar', alpha=0.7)
plt.title("Average Waiting Time per CPU Scheduler(out_input1)")
plt.xlabel("CPU Schedule")
plt.ylabel("Average Waiting Time")
plt.grid(True)
plt.show()

# 資料
turnaround_time_data = {
    "ID": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 20, 27, 29],
    "FCFS": [23, 15, 25, 22, 16, 26, 5, 16, 23, 9, 16, 19, 16, 22, 20],
    "RR": [22, 10, 22, 29, 22, 33, 20, 3, 16, 17, 45, 4, 20, 34, 37],
    "SJF": [9, 7, 5, 10, 10, 25, 10, 3, 2, 4, 57, 5, 8, 15, 21],
    "SRTF": [4, 2, 5, 10, 3, 25, 11, 1, 2, 5, 57, 1, 3, 25, 25],
    "HRRN": [23, 7, 19, 18, 16, 29, 5, 4, 13, 10, 26, 5, 16, 15, 26],
    "PPRR": [4, 2, 17, 4, 14, 27, 16, 56, 11, 4, 53, 1, 43, 16, 10]
}

# 转换成DataFrame
turnaround_time_df = pd.DataFrame(turnaround_time_data)

# 绘制箱型图
turnaround_time_df.drop(columns=["ID"]).boxplot()
plt.title("Turnaround Time Boxplot(out_input1)")
plt.ylabel("Time")
plt.xlabel("CPU Schedule")
plt.xticks(rotation=45)
plt.show()