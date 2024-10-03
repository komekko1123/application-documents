#11027209 資訊三乙 巫年巨
def write_file(filename,methodnumber,write_list):
  file_name = "out_" + filename
  method_list = ["FIFO", "LRU", "Least Frequently Used Page Replacement", "Most Frequently Used Page Replacement ", "Least Frequently Used LRU Page Replacement"] 
  with open(file_name, 'w') as f:
      if methodnumber == 6:

        for i in range(len(write_list)):
          f.write("--------------{0}-----------------------\n".format(method_list[i]))
          for j in range(len(write_list[i][0][0])): #write_list 這是00[PG_REF_STR,PG_FRAME,PG_FAULT ,Pg_fault_name,] pg_replace_num, pg_frame_number
            f.write("{0}\t{1}{2}\n".format(write_list[i][0][0][j][0], ''.join(write_list[i][0][0][j][1]), write_list[i][0][0][j][2])) 
          f.write("Page Fault = {0}  Page Replaces = {1}  Page Frames = {2}".format(write_list[i][0][1], write_list[i][0][2], write_list[i][0][3])) 
          if i != (len(write_list)) - 1:
            f.write("\n\n")
          else:
            f.write("\n")
      else:
        f.write("--------------{0}-----------------------\n".format(method_list[methodnumber-1]))
        for j in range(len(write_list[0][0])): #write_list 這是00[PG_REF_STR,PG_FRAME,PG_FAULT ,Pg_fault_name,] pg_replace_num, pg_frame_number
          f.write("{0}\t{1}{2}\n".format(write_list[0][0][j][0], ''.join(write_list[0][0][j][1]), write_list[0][0][j][2])) 
        f.write("Page Fault = {0}  Page Replaces = {1}  Page Frames = {2}\n".format(write_list[0][1], write_list[0][2], write_list[0][3]))

def PAGE_REPLACEMENT(methodnumber,page_ref_str,PageFrameNumber):
  page_replace = 0
  page_fault = 0
  Pageframe_Str_list = [] 
  for i in range(len(page_ref_str)):
    Pageframe_Str_list.append([page_ref_str[i],[],' ']) #PG_REF_STR,PG_FRAME,PG_FAULT
  page_frame = []
  answer_list = []
  if methodnumber == 1: # FCFS
    for i in range ( len(page_ref_str) ):
      if Pageframe_Str_list[i][0] not in page_frame and len(page_frame) != PageFrameNumber: #一開始加入的狀況
        page_frame.append(page_ref_str[i])
        Pageframe_Str_list[i][2] = '\tF'
        page_fault = page_fault + 1
      elif Pageframe_Str_list[i][0] not in page_frame and len(page_frame) == PageFrameNumber: #Replace的狀況
        page_frame.pop(0)
        page_frame.append(page_ref_str[i])
        Pageframe_Str_list[i][2] = '\tF'
        page_replace = page_replace + 1
        page_fault = page_fault + 1
      elif Pageframe_Str_list[i][0] in page_frame : # 正常狀況  
        Pageframe_Str_list[i][2] = ''
      templist = []
      for o in page_frame:
        templist.append(o)
      Pageframe_Str_list[i][1] = templist[::-1] #reverse
    answer_list.append( [ Pageframe_Str_list,page_fault,page_replace,PageFrameNumber ])
    
  elif methodnumber == 2: # LRU
    for i in range ( len(page_ref_str) ):
      if Pageframe_Str_list[i][0] not in page_frame and len(page_frame) != PageFrameNumber: #一開始加入的狀況
        Pageframe_Str_list[i][2] = '\tF'
        page_fault = page_fault + 1
      elif Pageframe_Str_list[i][0] not in page_frame and len(page_frame) == PageFrameNumber: #Replace的狀況
        index_list = []
        for j in range(len(page_frame)): #可取代的情況先把依照queue全部
          index_list.append(False)
        for k in range(i-1,-1,-1):
          if Pageframe_Str_list[i][0] in page_frame: #該str in frame 
            index_del = page_frame.index(Pageframe_Str_list[i][0])
            index_list[index_del] = True
          if index_list.count(True) == len(page_frame) - 1:
            break

        index_to_replace = index_list.index(False)
        page_frame.pop(index_to_replace)
        Pageframe_Str_list[i][2] = '\tF'
        page_replace = page_replace + 1
        page_fault = page_fault + 1
      elif Pageframe_Str_list[i][0] in page_frame : # 正常狀況
        Pageframe_Str_list[i][2] = ''
        page_frame.pop(page_frame.index(Pageframe_Str_list[i][0]))

      page_frame.append(page_ref_str[i])
      templist = []
      for o in page_frame:
        templist.append(o)
      Pageframe_Str_list[i][1] = templist[::-1]
    answer_list.append( [ Pageframe_Str_list,page_fault,page_replace,PageFrameNumber ])       
    
  elif methodnumber == 3: # LFU + FIFO
    count_dict = {}
    page_frame_has_index = []
    for i in range ( len(page_ref_str) ):
      if Pageframe_Str_list[i][0] not in page_frame and len(page_frame) != PageFrameNumber: #一開始加入的狀況
        page_frame.append(page_ref_str[i]) 
        page_frame_has_index.append([page_ref_str[i],i])
        Pageframe_Str_list[i][2] = '\tF'
        page_fault = page_fault + 1
      elif Pageframe_Str_list[i][0] not in page_frame and len(page_frame) == PageFrameNumber: #Replace的狀況按照lfu在fifo
        index_list = []
        very_big = float('inf')
        least = float('inf')
        index_to_replace = 0
        for _ in range(len(page_frame)): #可取代的情況先把依照queue全部
          index_list.append(very_big)
        for j in range(len(page_frame)):
          index_list[j] = count_dict[page_frame[j]] #應該都會有
          if least > index_list[j]:
            least = index_list[j]
            index_to_replace = j 
        if index_list.count(least) > 1: #代表有兩個一樣，要做FIFO做
          index_to_del = float('inf')
          for k in range(len(page_frame)):
            if index_list[k] == least :
              if index_to_del > page_frame_has_index[k][1]: #比較index找出最小
                index_to_del = page_frame_has_index[k][1]         
                index_to_replace = k                              
                                                                  
        count_dict[ page_frame[index_to_replace]] = 0   
        page_frame.pop(index_to_replace)        
        page_frame.append(page_ref_str[i]) 
        page_frame_has_index.pop(index_to_replace)
        page_frame_has_index.append([page_ref_str[i],i])
        Pageframe_Str_list[i][2] = '\tF'
        page_replace = page_replace + 1
        page_fault = page_fault + 1  
      elif Pageframe_Str_list[i][0] in page_frame: #更新index
       # index_to_update = page_frame.index(Pageframe_Str_list[i][0])
       # page_frame_has_index[index_to_update][1] = i
        Pageframe_Str_list[i][2] = ''

      if page_ref_str[i] not in count_dict:
        count_dict[page_ref_str[i]] = 1
      else:
        count_dict[page_ref_str[i]] += 1 # 更新count

      templist = []
      for o in page_frame:
        templist.append(o)
      Pageframe_Str_list[i][1] = templist[::-1]            
    answer_list.append( [ Pageframe_Str_list,page_fault,page_replace,PageFrameNumber ])     
  elif methodnumber == 4: # MFU + FIFO
    count_dict = {}
    page_frame_has_index = []
    for i in range ( len(page_ref_str) ):
      if Pageframe_Str_list[i][0] not in page_frame and len(page_frame) != PageFrameNumber: #一開始加入的狀況
        page_frame.append(page_ref_str[i])         
        page_frame_has_index.append([page_ref_str[i],i])
        Pageframe_Str_list[i][2] = '\tF'
        page_fault = page_fault + 1
      elif Pageframe_Str_list[i][0] not in page_frame and len(page_frame) == PageFrameNumber: #Replace的狀況按照mfu在fifo
        index_list = []
        very_small = -1
        bigest = -1
        index_to_replace = 0
        for _ in range(len(page_frame)): #可取代的情況先把依照queue全部
          index_list.append(very_small)
        for j in range(len(page_frame)):
          index_list[j] = count_dict[page_frame[j]] #應該都會有
          if bigest < index_list[j]:
            bigest = index_list[j]
            index_to_replace = j 
        if index_list.count(bigest) > 1: #代表有兩個一樣，要做FIFO做
          index_to_del = float('inf')
          for k in range(len(page_frame)):
            if index_list[k] == bigest :
              if index_to_del > page_frame_has_index[k][1]: #比較index找出最小
                index_to_del = page_frame_has_index[k][1]
                index_to_replace = k

        count_dict[ page_frame[index_to_replace]] = 0   
        page_frame.pop(index_to_replace)      
        page_frame.append(page_ref_str[i]) 
        page_frame_has_index.pop(index_to_replace)
        page_frame_has_index.append([page_ref_str[i],i])
        Pageframe_Str_list[i][2] = '\tF'
        page_replace = page_replace + 1
        page_fault = page_fault + 1  
      elif Pageframe_Str_list[i][0] in page_frame: #更新index
      #  index_to_update = page_frame.index(Pageframe_Str_list[i][0])
      #  page_frame_has_index[index_to_update][1] = i
        Pageframe_Str_list[i][2] = ''


      if page_ref_str[i] not in count_dict:
        count_dict[page_ref_str[i]] = 1
      else:
        count_dict[page_ref_str[i]] += 1 # 更新count
      templist = []
      for o in page_frame:
        templist.append(o)
      Pageframe_Str_list[i][1] = templist[::-1]
    answer_list.append( [ Pageframe_Str_list,page_fault,page_replace,PageFrameNumber ])     

  elif methodnumber == 5: # LFU + LRU
    count_dict = {}
    for i in range ( len(page_ref_str) ):
      if Pageframe_Str_list[i][0] not in page_frame and len(page_frame) != PageFrameNumber: #一開始加入的狀況
        Pageframe_Str_list[i][2] = '\tF'
        page_fault = page_fault + 1
      elif Pageframe_Str_list[i][0] not in page_frame and len(page_frame) == PageFrameNumber: #Replace的狀況按照lfu在LRU
        index_list = []
        very_big = float('inf')
        least = float('inf')
        index_to_replace = 0
        for _ in range(len(page_frame)): #可取代的情況先把依照queue全部
          index_list.append(very_big)
        for j in range(len(page_frame)):
          index_list[j] = count_dict[page_frame[j]] #應該都會有
          if least > index_list[j]:
            least = index_list[j]
            index_to_replace = j 
        if index_list.count(least) > 1: #代表有兩個一樣，改去做LRU
          index_lru = []
          for j in range(len(page_frame)):
            if index_list[j] == least :
              index_lru.append(False) #放入要比較的字
            else:
              index_lru.append(True)
          for k in range(i-1,-1,-1):
            if Pageframe_Str_list[i][0] in page_frame: #該str in frame
              index_del = page_frame.index(Pageframe_Str_list[i][0])
              index_lru[index_del] = True
            if index_lru.count(True) == len(page_frame) - 1:
              break
          index_to_replace = index_lru.index(False)

        count_dict[ page_frame[index_to_replace]] = 0   #可能要加
        page_frame.pop(index_to_replace)        
        Pageframe_Str_list[i][2] = '\tF'
        page_replace = page_replace + 1
        page_fault = page_fault + 1  
      elif Pageframe_Str_list[i][0] in page_frame:
        Pageframe_Str_list[i][2] = ''
        page_frame.pop(page_frame.index(Pageframe_Str_list[i][0]))

      page_frame.append(page_ref_str[i])  
      if page_ref_str[i] not in count_dict:
        count_dict[page_ref_str[i]] = 1
      else:
        count_dict[page_ref_str[i]] += 1 # 更新count
      templist = []
      for o in page_frame:
        templist.append(o)
      Pageframe_Str_list[i][1] = templist[::-1]
    answer_list.append( [ Pageframe_Str_list,page_fault,page_replace,PageFrameNumber ])   
  elif methodnumber == 6: # ALL
    answer_list = []
    for i in range(5):
      answer_list.append(PAGE_REPLACEMENT(i+1,page_ref_str,PageFrameNumber))
    return answer_list
  else:
    return
  return answer_list

def main():
  while True:
    filename = input( "請輸入檔案名稱\n")
    if filename.find(".txt") == -1: # 沒有.txt就補上
      filename = filename + ".txt"    
    with open(filename, 'r') as f:
      line = f.readline()
      methodnumber,pageframe = line.split()
      Pg_ref_str = f.readline() # 這是sequence string      
      Pg_ref_str = Pg_ref_str.strip() #去除換行
    write_list = PAGE_REPLACEMENT(int(methodnumber), Pg_ref_str,int(pageframe))
    write_file(filename,int(methodnumber),write_list)
    print("\n結束\n")
if __name__ == '__main__':
  main()