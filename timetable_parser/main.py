from parser import Parser


def main():

    time_table = Parser().get_timetable(720)
    # print(time_table)

    for week in time_table:
        for day in time_table[week]:
            print(f'{day.capitalize()}:')
            for subject in time_table[week][day]:
                for key, value in subject.items():
                    print(f'\t{key}: {value}')
                print()
            print()
            print()



if __name__ == '__main__':
    main()