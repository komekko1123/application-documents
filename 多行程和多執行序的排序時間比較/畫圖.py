import matplotlib.pyplot as plt

# 提供的數據
inputs = [  "10000", "100000", "500000", "1000000"]
methods = ['Method 1', 'Method 2', 'Method 3', 'Method 4']

method1_times = [4.1640284061431885, 433.3124349117279, 11833.996987581253, 55369.779307603836]
method2_times = [3.9, 80.59299945831299, 609.9179260730743, 2420.557797431946]
method3_times = [4, 20.738460779190063, 147.255380153656, 494.0411880016327]
method4_times = [4.2, 60.80932831764221, 420.4910342693329, 2110.249349117279]

colors = ['b', 'g', 'r', 'c']

# 繪製圖表
plt.figure(figsize=(10, 6))

for i, method_times in enumerate([method1_times, method2_times, method3_times, method4_times]):
    plt.plot(inputs, method_times, marker='o', linestyle='-', color=colors[i], label=methods[i])

plt.title('OS homework 1  with different method')
plt.xlabel('Input Size')
plt.ylabel('CPU Time (s)')
#plt.yscale('log')
plt.ylim(0, 10000)  # 將 y 軸的範圍設置為 0 到 10000
plt.yticks(range(0, 10000, 1000))  # 將 y 軸刻度設置為 0 到 10000，間隔為 1000
plt.grid(True, which="both", ls="--")
plt.legend()
plt.tight_layout()
plt.show()