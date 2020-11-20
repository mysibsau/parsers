from parser import Parser


def main():

    session = Parser().get_session(5080)

    for day in session:
        for key, value in day.items():
            print(key, ':', value)
        print()
        print()




if __name__ == '__main__':
    main()