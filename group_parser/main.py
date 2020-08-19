from group_parser import GroupParser
import threading
import time

begin = time.time()

gp = GroupParser()

for i in range(0, 6000):
    x = threading.Thread(target=gp.get_name_groups_by_id, args=(i, ))
    x.start()

gp.save_data_in_json()

end = time.time()

print(f'Time: {end-begin}')