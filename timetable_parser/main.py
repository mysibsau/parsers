from parser import Parser


def main():
    p = Parser()

    # БПИ
    id_group_bpi = 5047

    # РС
    id_group_rs = 5080
    time_table = p.get_timetable_for_group(id_group_bpi)

    for week in time_table['timetable'].keys():
        for day in time_table['timetable'][week].keys():
            print(f'{day.capitalize()}:')
            for subject in time_table['timetable'][week][day]:
                for key, value in subject.items():
                    print(f'\t{key}: {value}')
                print()
            print()
            print()



if __name__ == '__main__':
    main()