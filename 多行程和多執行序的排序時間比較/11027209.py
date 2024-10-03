#11027209 資訊三乙 巫年巨
from multiprocessing import Manager,Pool,Process
import time
import datetime
import threading  
def bubblesort(arr):
  has_swap = False
  for i in range(len(arr)):
    has_swap = False
    for j in range(0,len(arr)-i-1):
      if arr[j] > arr[j+1] :
        has_swap = True
        arr[j], arr[j+1] = arr[j+1], arr[j] #swap
    if has_swap == False:
      break
  return arr

def merge(arr1, arr2):
  result = []
  i = 0
  j = 0
  while i < len(arr1) and j < len(arr2):
      if arr1[i] < arr2[j]:
          result.append(arr1[i])
          i += 1
      else:
          result.append(arr2[j])
          j += 1
  result.extend(arr1[i:]) # 把還沒加到的放進去如果i or j超過size就捨都不會放
  result.extend(arr2[j:])
  return result

def read_file_array(filename):
  arr = []
  file_name = filename + ".txt"
  with open(file_name, 'r') as f:
     for line in f.readlines():
        data = int(line.strip())  # Convert string to integer
        arr.append(data)
  return arr

def write_file_array(arr,total_time,filename,methodnumber):
  file_name = filename + "_output" + str(methodnumber) + ".txt"
  with open(file_name, 'w') as f:
     f.write("Sort : \n")
     for i in arr:
       f.write(str(i) + "\n")
     f.write("CPU Time = {}\n".format(total_time))
     f.write("Output Time = {} ".format( datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))) ) )
  return arr

def divarray(arr,k):
  if k > 0 and k < len(arr):
    div_arrsize = len(arr) // k
  else: 
    k = 1
    div_arrsize = len(arr) // k # 錯誤的情況就只分一份
  div_arr = [] # 放array群等等拿去做mergesort
  for i in range(k):
    start = i * div_arrsize # 分割得開頭
    if i != k - 1: # 除得進
      end = start + div_arrsize 
    else:    # 可能會有餘數(除不進)的狀況，跟最後一份合併
      end = len(arr)
    sub_arr = arr[start:end]
    div_arr.append(sub_arr)
  return div_arr

def bubblesortformulti(arr,result):
  has_swap = False
  for i in range(len(arr)):
    has_swap = False
    for j in range(0,len(arr)-i-1):
      if arr[j] > arr[j+1] :
        has_swap = True
        arr[j], arr[j+1] = arr[j+1], arr[j] #swap
    if has_swap == False:
      break
  result.append(arr)

def mergeformulti(arr1, arr2,resulta): #因為不能拿return值故使用call by reference來拿值
  i = 0
  j = 0
  result = []
  while i < len(arr1) and j < len(arr2):
      if arr1[i] < arr2[j]:
          result.append(arr1[i])
          i += 1
      else:
          result.append(arr2[j])
          j += 1
  result.extend(arr1[i:]) # 把還沒加到的放進去如果i or j超過size就捨都不會放
  result.extend(arr2[j:])
  resulta.append(result)


def method1(filename):
  arr = read_file_array(filename)
  start_time = time.time()
  bubblesort(arr)
  end_time = time.time()
  total_time = end_time - start_time
  write_file_array(arr,total_time,filename,1)
  
def method2(k,filename): 
  arr = read_file_array(filename)
  start_time = time.time()
  div_arr = divarray(arr,k) # 放分割array群
  for i in range(k): 
    bubblesort(div_arr[i]) 
  while len(div_arr) >= 2:
    for _ in range( len(div_arr) // 2 ): # 用// 把奇數便整數會
      arr1 = div_arr.pop(1)
      arr2 = div_arr.pop(0)
      div_arr.append( merge(arr1, arr2 ) )  #把merge完的結果放回div_arr到最後就只會剩下一個
  merge_sort_arr = div_arr[0]
  end_time = time.time()
  total_time = end_time - start_time
  write_file_array(merge_sort_arr,total_time,filename,2)


def method3(k,filename):
  arr = read_file_array(filename)
  manager = Manager()
  arr = divarray(arr,k) # 放分割array群
  div_arr = manager.list([])
  process_list = []
  start_time = time.time()
  # with Pool(k) as pool: #方法2
  #   for i in range(k): # 用// 把奇數便整數會
  #     div_arr.append(pool.apply_async(bubblesort,(arr[i],)).get())
  #   pool.close()
  #   pool.join()

  for i in range(k): #方法1
    p = Process(target=bubblesortformulti, args=(arr[i],div_arr))
    p.start()
    process_list.append(p)
  for p in process_list:
    p.join()
  process_list.clear()

  # while len(div_arr) >= 2: #方法1
  #     for _ in range( len(div_arr) // 2 ): # 用// 把奇數便整數會
  #       temp_arr1 = div_arr.pop(1)
  #       temp_arr2 = div_arr.pop(0)
  #       p = Process(target=mergeformultiprocess, args=(temp_arr1,temp_arr2,div_arr))
  #       p.start()
  #       process_list.append(p)
  #     for p in process_list:
  #       p.join()
  #     process_list.clear()
  while len(div_arr) >= 2: #方法2
    with Pool(len(div_arr) // 2) as pool:
      for _ in range( len(div_arr) // 2 ): # 用// 把奇數便整數會
        temp_arr1 = div_arr.pop(1)
        temp_arr2 = div_arr.pop(0)
        div_arr.append(pool.apply_async(merge,(temp_arr1,temp_arr2)).get())
      pool.close()
      pool.join()

  merge_sort_arr = div_arr[0]
  end_time = time.time()
  total_time = end_time - start_time
  write_file_array(merge_sort_arr,total_time,filename,3)


def method4(k,filename):
  arr = read_file_array(filename)
  thread_list = []
  start_time = time.time()
  div_arr = divarray(arr,k) # 放分割array群
  for i in range( k ): # 用// 把奇數便整數會
    thread = threading.Thread(target=bubblesort, args=(div_arr[i],))
    thread.start()
    thread_list.append(thread)
  for t in thread_list:
    t.join()
  thread_list.clear()
  while len(div_arr) >= 2:
    for i in range( len(div_arr) // 2 ): # 用// 把奇數便整數會
      arr1 = div_arr.pop(1)
      arr2 = div_arr.pop(0)
      thread = threading.Thread(target=mergeformulti,args=(arr1,arr2,div_arr) ) # thread不好return故在寫了一個function
      thread.start()
      thread_list.append(thread)
    for t in thread_list:
        t.join()
    thread_list.clear()     
  merge_sort_arr = div_arr[0]
  end_time = time.time()
  total_time = end_time - start_time
  write_file_array(merge_sort_arr,total_time,filename,4)

def main():
  filename = input( "請輸入檔案名稱\n")
  k = int(input("請輸入要切成幾份:\n"))
  methodnumber = int(input("請輸入方法編號:(方法1, 方法2, 方法3, 方法4)\n"))
  while True:    
    print("開始跑方法")
    if methodnumber == 1:
      method1(filename)
    elif methodnumber == 2:
      method2(k,filename)
    elif methodnumber == 3:
      method3(k,filename)
    elif methodnumber == 4:
      method4(k,filename)
    elif methodnumber == 0:
      break
    else:
      print("Invalid method number")  
    print("結束")
    filename = input( "請輸入檔案名稱\n")
    k = int(input("請輸入要切成幾份:\n"))
    methodnumber = int(input("請輸入方法編號:(方法1, 方法2, 方法3, 方法4)\n"))

if __name__ == '__main__':
  main()

