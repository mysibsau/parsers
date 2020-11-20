from parser import ParseConsultation


def main():

    consultation = ParseConsultation().get_consultation(2569)

    if consultation:

        for week in consultation:
            print(week)
            for day in consultation[week]:
                for key, value in day.items():
                    print(key, ':', value)
                print()
            print()
            print()


if __name__ == '__main__':
    main()