from professor_parser import ProfessorParser
import time


begin = time.time()

pp = ProfessorParser()

pp.set_professors()
pp.save_data_in_csv()

final_time = time.time() - begin
print(f'Time: {final_time // 60} min({final_time} sec)')
