import sqlite3


def main(args=[]):
    connection = sqlite3.connect('agricolaif.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    connection.close()


if __name__ == '__main__':
    main()