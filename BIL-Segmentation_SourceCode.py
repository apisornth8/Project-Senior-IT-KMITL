
#Note
"""Run on Google Colab >https://colab.research.google.com/<"""

import random, math
import pandas as pd
import operator as opt
import numpy as np
import time

# rule table : mask[BitofIndex], value[BitofIndex]
#Parameter
BITOFINDEX:int = 16 # Bit of field = 2**n

BITOFRULE:int = 100 # Number rule

INPUT_SIZE: int = 2**BITOFINDEX
def convert2(input: int,count: int) -> list:
    num:list = [0]*count
    for i in range(len(num)):
        bit:int = input % 2
        input:int = input // 2
        num[count-1-i] = bit
    return num

def GenRule(BitOfindex: int) -> dict:
    value = [0]*BitOfindex
    mask = [0]*BitOfindex
    for i in range(BitOfindex):
        value[i] = random.randint(0,1)
        mask[i] = random.randint(0,1)
    return {"value":value, "mask":mask}

# map_rule เราทำเพื่อเช็ค input ที่รับเข้ามาตรงกันกับเงื่อนไขหรือไม่ 
def map_rule(index: int, value: list, mask: list, BitOfindex: int) -> int:
    # ans : int = 1
    indexbase2:list = convert2(index, BitOfindex);
    
    # if index == 0:
    #     print('index : ', index)
    #     print('bit_of_index : ', BitOfindex)
    #     print('value , mask ', value, mask)


    # for i in range(BitOfindex):
    #     check_bit:bool = (mask[i] == 1) and (value[i] != indexbase2[i])
    #     if (check_bit):
    #         ans = 0
    #         break

    # return 0 แสดงว่า มีความผิดปกติ (Don't care)
    # (mask[i] == 1) จะถูกต้องหรือตรงนั้นเอง (Interested for Checking)
    # (value[i] != indexbase2[i]) แสดงว่ามันไม่ตรงหรือผิด
    # ถ้า output return เป็น 0 คือ Don't care เราจะ set ให้เป็น 1 ไปเลย
    # print((np.array(mask) & np.array(value)) & np.array(indexbase2))
    ans = all((np.array(mask) & np.array(value)) & np.array(indexbase2))
    # all มีบิทไหนเป็น 0 จะรีเทิร์น false ออกมาเพราะมันไม่เป็นไปตาม Value
    
    return ans
    # ans จะ  turn ค่า 0 ที่อยู่ return ออกมาข้างใน list คือ ค่าที่ไม่ตรงกับกฏที่กำหนดไว้ 
    # แต่ถ้า ค่าเป็น 1 ที่อยู่ return ออกมาข้างใน list คือ ค่าที่ตรงกับกฏที่กำหนดไว้

def partition_input(input:list, bit_of_index:int, number_of_segment:int, segment_partition_size:list):
    seg_input = [0] * number_of_segment

    # segment_size:int = int(bit_of_index / number_of_segment)
    # print('segment_size : ', segment_size)

    temp_segment_size = 0
    for ns in range(number_of_segment):  
        binary_value = input[temp_segment_size : temp_segment_size + segment_partition_size[ns]]
        temp_segment_size = temp_segment_size + segment_partition_size[ns]
        # print('binary_value : ', binary_value)
        for i, value in enumerate(binary_value):
              seg_input[ns] += int(value * math.pow(2, (segment_partition_size[ns]-i-1)))
    return seg_input

def create_rule_table(bit_of_index:int, bit_of_rule:int):
    rt = []
    """Generate Rule"""
    for i in range(bit_of_rule):
        """i is rule index"""
        # print("Rule NO: {}".format(i));
        rule = GenRule(bit_of_index)
        rt.append(rule)
    return rt

rt = create_rule_table(bit_of_index=16, bit_of_rule=1000)
#--------------------------------------------------------------------------------------
"""เช็ค index ค่าที่ = 0"""
for i, rt_val in enumerate(rt):
  print('rule ', i+1)
  value = [ j+1 for j in range(len(rt_val['value'])) if rt_val['value'][j] == 0]
  mask = [ j+1 for j in range(len(rt_val['mask'])) if rt_val['mask'][j] == 0]
  print('value : ', value)
  print('mask  : ', mask)
  
"""เช็ค index ค่าที่ = 1"""
for i, rt_val in enumerate(rt):
  print('rule ', i+1)
  value = [ j+1 for j in range(len(rt_val['value'])) if rt_val['value'][j] == 1]
  mask = [ j+1 for j in range(len(rt_val['mask'])) if rt_val['mask'][j] == 1]
  print('value : ', value)
  print('mask  : ', mask)
#--------------------------------------------------------------------------------------
def create_bil_table_function(field_size:int, rule_table: list, bit_of_index:int, bit_of_rule:int):
    bil_table = dict()


    for input in range(field_size):
        index_field: list = [1]*bit_of_rule
        for rule_no in range(bit_of_rule):
          
          check_maprule:int = map_rule(input, rule_table[rule_no]["value"], rule_table[rule_no]["mask"], bit_of_index)
          index_field[rule_no] = check_maprule
        
        bil_table[input] = index_field
        # print(len(bil_table), bil_table)
    return bil_table
    
def search_bil_function(input: int, bil_table: dict) -> list:
  """
    BIL Search function:
    1. search input in BIL table 
    2. identify bitmap result to ruleID
    3. FCFS (First come First Serve) first ruleID as match rule
  """
  rule_id = []
  for i, bit_value in enumerate(bil_table[input]):
    if bit_value == 1:
      rule_id.append(i)
  
  if len(rule_id) > 0:
    return rule_id[0]  
  else:
    return '-'
def bil_search_algorithm(input_size:int, field_size: int, rule_table:list,bit_of_rule:int):
    
    bil_search_result = []
    start = time.time()
    bil_table = create_bil_table_function(field_size=2**BITOFINDEX, 
                                          rule_table=rt,  
                                          bit_of_index=BITOFINDEX,
                                          bit_of_rule=10000)
    end = time.time()
    print('BIL Table create time : ', end - start , ' seconds')

    
    print('BIL_Table size : ', len((bil_table)*bit_of_rule/8,),' bytes')
    
    """ loop test input subject in range (0 - 65536) """
    for input in range(input_size):
        """
           "ans" is เป็นตัวแปรที่เก็บว่า input นี้มี rule ขอใดข้อนึ่ง invalid ยัง ถ้าไม่มี จะเปลี่ยนเป็น 0 
           "result_checkmaprule" is ตัวแปรที่เก็บผลลัพธ์ ว่า 
           input นี้เมื่อเช็คกับ rule แต่ละข้อ ว่า ข้อไหน ให้ผ่าน ไม่ให้ผ่านบ้าง มีขนาดเท่ากับ จำนวนกฎ
        """

        ans = search_bil_function(input, bil_table)
      
        bil_search_result.append(ans)

    return bil_search_result

def bil_table_create_for_none_equal_segmentation(rt: list, bit_of_rule: int, bit_of_index:int, number_of_segment:int, segment_partition_size=list):
    
    if sum(segment_partition_size) != bit_of_index:
      raise Exception("sum(segment_partition_size) != bit_of_index") 
    if len(segment_partition_size) != number_of_segment:
      raise Exception("len(segment_partition_size) != number_of_segment")

    seg_rt = [list()] * number_of_segment

    # print('len(rt) : ', len(rt))
    for rule_no in range(bit_of_rule):
        temp_rule = rt[rule_no]
        # print('rule_no : ', rule_no)
        
        temp_segment_size = 0
        for ns in range(number_of_segment):
            # print(ns)
            # print('temp_rule : ', temp_rule)
            # print('range segment : ', ns*segment_size, (ns+1)*segment_size)
            
            value = temp_rule['value'][temp_segment_size: temp_segment_size + segment_partition_size[ns]]
            mask = temp_rule['mask'][temp_segment_size: temp_segment_size + segment_partition_size[ns]]

            temp_segment_size = temp_segment_size + segment_partition_size[ns]

            # print([{'value': value, 'mask':mask}])
            
            seg_rt[ns] = seg_rt[ns] + [{'value': value,
                          'mask':mask}]
                 
    return seg_rt
        
import numpy as np
def bil_search_on_segmentation_algorithm_for_none_equal_segmentation(input_size:int, bit_of_index: int,bit_of_rule:int, rule_table:list, number_of_segment=6, segment_partition_size=list):
    
    bil_search_result = []

    start = time.time()

    # segment_size:int = bit_of_index//number_of_segment

    seg_table = bil_table_create_for_none_equal_segmentation(rt=rule_table, 
                                                  bit_of_index=bit_of_index, 
                                                  bit_of_rule=bit_of_rule, 
                                                  number_of_segment=number_of_segment,
                                                  segment_partition_size=segment_partition_size)
    
    seg_bil_table = [list()] * number_of_segment
    for i in range(number_of_segment):
      #  print('number_of_segment : ',i)
      #  print('segment table : ', seg_table[i])
      seg_bil_table[i] = create_bil_table_function(field_size=2**segment_partition_size[i], 
                                                    rule_table=seg_table[i], 
                                                    bit_of_index=segment_partition_size[i], 
                                                    bit_of_rule=bit_of_rule)
    end = time.time()

    print('BIL Table create time: {:.7f} seconds'.format(end - start))
    #print('BIL_Table size: {:.3f} bytes'.format(len([j for i in seg_bil_table for j in i])*bit_of_rule/8))
    

    #print('seg_bil_table : ', seg_bil_table)
    
    #print('seg_table : ', seg_table)
    """ loop test input subject in range (0 - 65536) """

    
    for input in range(input_size):
        binary_input = convert2(input, bit_of_index)
        binary_partition_input = partition_input(input=binary_input, 
                                                 bit_of_index=bit_of_index,
                                                 number_of_segment=number_of_segment,
                                                 segment_partition_size=segment_partition_size)
        
        after_AND_operation_result = [1]*bit_of_rule
        start = time.time()
        for ns in range(number_of_segment):

            match_rule_ns = seg_bil_table[ns][binary_partition_input[ns]]
            for i in range(bit_of_rule):
              after_AND_operation_result[i] = after_AND_operation_result[i] and match_rule_ns[i]

        rule_id = []
        for i, bit_value in enumerate(after_AND_operation_result):
          if bit_value == 1:
            rule_id.append(i)

        if len(rule_id) > 0:
          bil_search_result.append(rule_id[0])
        else:
          bil_search_result.append('-')
    end = time.time()
    print('BIL Search time: {:.7f} seconds'.format(end - start))
    return bil_search_result

#Test runtime
time_search_1 = bil_search_on_segmentation_algorithm_for_none_equal_segmentation(input_size=2**BITOFINDEX, 
                                     bit_of_index=BITOFINDEX,
                                     bit_of_rule=500,
                                     rule_table=rt,
                                     number_of_segment=2,
                                    segment_partition_size=[14,2])