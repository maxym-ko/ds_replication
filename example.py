import time

import psycopg2
from faker import Faker

MASTER_DB_PARAMS = {
    'dbname': 'postgres',
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

REPLICA_DB_PARAMS = {
    'dbname': 'postgres',
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'port': '5433'
}


def __write_to_db():
    faker = Faker()

    master_conn = psycopg2.connect(**MASTER_DB_PARAMS)
    with master_conn.cursor() as cursor:
        cursor.executemany("INSERT INTO cars (brand, model, year) VALUES (%s, %s, %s)",
                           [(faker.name(), faker.word(), faker.year())])
        master_conn.commit()


def __read_db():
    replica_conn = psycopg2.connect(**REPLICA_DB_PARAMS)
    with replica_conn.cursor() as cursor:
        cursor.execute('SELECT * FROM cars')
        results = cursor.fetchall()

        return results


def main():
    print(f'Before: {__read_db()}')

    __write_to_db()
    time.sleep(2)

    print(f'After: {__read_db()}')


if __name__ == "__main__":
    main()
