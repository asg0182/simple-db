import argparse
import sqlite3
from faker import Faker


fake = Faker()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, default=1000, help="Count of person for creation")
    return parser.parse_args()


def create_db():
    con = sqlite3.connect("example.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    tables = res.fetchone()
    if tables is None:
        cur.execute("CREATE TABLE persones(name, date_of_birth, country, address)")
    elif not tables is None and "persones" not in tables:
        cur.execute("CREATE TABLE persones(name, date_of_birth, country, address)")
    return cur, con


def create_person():
    return (fake.name(), fake.date_of_birth(), fake.country(), fake.address())


def main():
    args = parse_args()
    count = args.count

    cur, con = create_db()
    data = []

    for _ in range(count):
        data.append(create_person())

    cur.executemany("INSERT INTO persones VALUES(?, ?, ?, ?)", data)
    con.commit()


if __name__=="__main__":
    main()
