from group_parser import GroupParser
import time

begin = time.time()
gp = GroupParser()

for i in range(0, 6000):
    gp.get_name_groups_by_id(i)

gp.save_data_in_json()

end = time.time()

print(f'Time: {end-begin}')
