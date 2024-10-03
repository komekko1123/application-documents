import pandas as pd
import matplotlib.pyplot as plt

# 第一組資料 (input1)
data1 = {
    "Algorithm": ["FIFO", "LRU", "LFU", "MFU", "LFU-LRU"],
    "Page Faults": [9, 10, 10, 9, 10],
    "Page Replaces": [6, 7, 7, 6, 7],
}

# 第二組資料 (input1)
data2 = {
    "Algorithm": ["FIFO", "LRU", "LFU", "MFU", "LFU-LRU"],
    "Page Faults": [10, 8, 8, 10, 8],
    "Page Replaces": [6, 4, 4, 6, 4],
}

# 轉換成DataFrame
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# 合併DataFrame
df1.set_index("Algorithm", inplace=True)
df2.set_index("Algorithm", inplace=True)

# 加上標籤區分
df1.columns = [f"{col} (Set 1)" for col in df1.columns]
df2.columns = [f"{col} (Set 2)" for col in df2.columns]

# 合併兩個DataFrame
combined_df = pd.concat([df1, df2], axis=1)

# 繪製 Page Faults 的直方圖 (input1)
combined_df[['Page Faults (Set 1)', 'Page Faults (Set 2)']].plot(kind='bar', alpha=0.7, figsize=(12, 8))
plt.title("Comparison of Page Faults (input1)")
plt.xlabel("Page Replacement Algorithm")
plt.ylabel("Page Faults")
plt.grid(True)
plt.xticks(rotation=45)
plt.show()

# 繪製 Page Replaces 的直方圖 (input1)
combined_df[['Page Replaces (Set 1)', 'Page Replaces (Set 2)']].plot(kind='bar', alpha=0.7, figsize=(12, 8))
plt.title("Comparison of Page Replaces (input1)")
plt.xlabel("Page Replacement Algorithm")
plt.ylabel("Page Replaces")
plt.grid(True)
plt.xticks(rotation=45)
plt.show()

# 第一組資料 (input2)
data3 = {
    "Algorithm": ["FIFO", "LRU", "LFU", "MFU", "LFU-LRU"],
    "Page Faults": [15, 12, 13, 15, 11],
    "Page Replaces": [12, 9, 10, 12, 8],
}

# 第二組資料 (input2)
data4 = {
    "Algorithm": ["FIFO", "LRU", "LFU", "MFU", "LFU-LRU"],
    "Page Faults": [10, 8, 9, 12, 9],
    "Page Replaces": [6, 4, 5, 8, 5],
}

# 轉換成DataFrame
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)

# 合併DataFrame
df3.set_index("Algorithm", inplace=True)
df4.set_index("Algorithm", inplace=True)

# 加上標籤區分
df3.columns = [f"{col} (Set 3)" for col in df3.columns]
df4.columns = [f"{col} (Set 4)" for col in df4.columns]

# 合併兩個DataFrame
combined_df2 = pd.concat([df3, df4], axis=1)

# 繪製 Page Faults 的直方圖 (input2)
combined_df2[['Page Faults (Set 3)', 'Page Faults (Set 4)']].plot(kind='bar', alpha=0.7, figsize=(12, 8))
plt.title("Comparison of Page Faults (input2)")
plt.xlabel("Page Replacement Algorithm")
plt.ylabel("Page Faults")
plt.grid(True)
plt.xticks(rotation=45)
plt.show()

# 繪製 Page Replaces 的直方圖 (input2)
combined_df2[['Page Replaces (Set 3)', 'Page Replaces (Set 4)']].plot(kind='bar', alpha=0.7, figsize=(12, 8))
plt.title("Comparison of Page Replaces (input2)")
plt.xlabel("Page Replacement Algorithm")
plt.ylabel("Page Replaces")
plt.grid(True)
plt.xticks(rotation=45)
plt.show()




# import pandas as pd
# import matplotlib.pyplot as plt

# # 第一組資料
# data1 = {
#     "Algorithm": ["FIFO", "LRU", "LFU", "MFU", "LFU-LRU"],
#     "Page Faults": [9, 10, 10, 9, 10],
#     "Page Replaces": [6, 7, 7, 6, 7],
#     "Page Frames": [3, 3, 3, 3, 3]
# }

# # 第二組資料
# data2 = {
#     "Algorithm": ["FIFO", "LRU", "LFU", "MFU", "LFU-LRU"],
#     "Page Faults": [10, 8, 8, 10, 8],
#     "Page Replaces": [6, 4, 4, 6, 4],
#     "Page Frames": [4, 4, 4, 4, 4]
# }

# # 轉換成DataFrame
# df1 = pd.DataFrame(data1)
# df2 = pd.DataFrame(data2)

# # 合併DataFrame
# df1.set_index("Algorithm", inplace=True)
# df2.set_index("Algorithm", inplace=True)

# # 加上標籤區分
# df1.columns = [f"{col} (Set 1)" for col in df1.columns]
# df2.columns = [f"{col} (Set 2)" for col in df2.columns]

# # 合併兩個DataFrame
# combined_df = pd.concat([df1, df2], axis=1)

# # 繪製直方圖
# combined_df.plot(kind='bar', alpha=0.7, figsize=(12, 8))
# plt.title("Comparison of Page Replacement Algorithms(input1)")
# plt.xlabel("Page Replacement Algorithm")
# plt.ylabel("Count")
# plt.grid(True)
# plt.xticks(rotation=45)
# plt.show()




# #-------------------------------------------

# # 第一組資料 (input1)
# data4 = {
#     "Algorithm": ["FIFO", "LRU", "LFU", "MFU", "LFU-LRU"],
#     "Page Faults": [10, 8, 9, 12, 9],
#     "Page Replaces": [6, 4, 5, 8, 5],
#     "Page Frames": [4, 4, 4, 4, 4]
# }

# # 第二組資料 (input2)
# data3 = {
#     "Algorithm": ["FIFO", "LRU", "LFU", "MFU", "LFU-LRU"],
#     "Page Faults": [15, 12, 13, 15, 11],
#     "Page Replaces": [12, 9, 10, 12, 8],
#     "Page Frames": [3, 3, 3, 3, 3]
# }

# # 轉換成DataFrame
# df3 = pd.DataFrame(data3)
# df4 = pd.DataFrame(data4)

# # 合併DataFrame
# df3.set_index("Algorithm", inplace=True)
# df4.set_index("Algorithm", inplace=True)

# # 加上標籤區分
# df3.columns = [f"{col} (Set 3)" for col in df3.columns]
# df4.columns = [f"{col} (Set 4)" for col in df4.columns]

# # 合併兩個DataFrame
# combined_df2 = pd.concat([df3, df4], axis=1)

# # 繪製直方圖
# combined_df2.plot(kind='bar', alpha=0.7, figsize=(12, 8))
# plt.title("Comparison of Page Replacement Algorithms(input2)")
# plt.xlabel("Page Replacement Algorithm")
# plt.ylabel("Count")
# plt.grid(True)
# plt.xticks(rotation=45)
# plt.show()