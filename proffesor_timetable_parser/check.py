from parser import Parser


def main():
    p = Parser()
    time_table = p.get_timetable(548)
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