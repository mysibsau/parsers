from group_parser import GroupParser
import time


begin = time.time()

gp = GroupParser()
gp.set_groups()
gp.save_data_in_json()

final_time = time.time() - begin
print(f'Time: {final_time // 60} min({final_time} sec)')
