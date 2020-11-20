from parser import Parser


def main():

    session = Parser().get_session(5047)

    if session:

        for day in session:
            for key, value in day.items():
                print(key, ':', value)
            print()
            print()




if __name__ == '__main__':
    main()