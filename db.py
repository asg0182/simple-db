import argparse
import sqlite3
from faker import Faker
from pprint import pprint

fake = Faker()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, default=0, help="Count of person for creation")
    return parser.parse_args()


def create_db():
    con = sqlite3.connect("example.db")
    cur = con.cursor()

    if not is_table_exists(cur, "persones"):
        create_table(con, cur)
    else:
        print("persones exists!")

    if not is_table_exists(cur, "country"):
        create_table(con, cur, "country", ["id", "country"])
    else:
        print("country exists")
        
    return cur, con


def is_table_exists(cur, table_name):
    query = f"SELECT 1 FROM sqlite_master WHERE name='{table_name}'"
    res = cur.execute(query).fetchone()
    if res is not None:
        return 1 in res
    return False


def create_table(con, cur, table_name = "persones", fields = ["name", "date_of_birth", "country_id", "address"]):
    fields_str = ", ".join(fields)
    table_script = f"CREATE TABLE {table_name} ({fields_str})"
    print(table_script)
    cur.execute(table_script)
    con.commit()


def create_person():
    return (fake.name(), fake.date_of_birth(), fake.country(), fake.address())


def main():
    args = parse_args()
    count = args.count

    cur, con = create_db()
    data = []
    countries = {}
    country_id = 0
    cur_country_id = 0

    if count > 0:
        for _ in range(count):
            name, date_of_birth, country, address = create_person()

            if country in countries:
                cur_country_id = countries.get(country)
            else:
                countries[country] = country_id
                cur_country_id = country_id
                country_id += 1

            data.append(
                (name, date_of_birth, cur_country_id, address)
            )

        data_countries = [
            (v, k) for k, v in countries.items()
        ]

        cur.executemany("INSERT INTO persones VALUES(?, ?, ?, ?)", data)
        cur.executemany("INSERT INTO country VALUES(?, ?)", data_countries)
        con.commit()

    join_query = """
    Select persones.name, country.country, persones.date_of_birth, persones.address From persones
    Join country On persones.country_id=country.id
"""
    cur.execute(join_query)
    res = cur.fetchall()
    pprint(res)
    


if __name__=="__main__":
    main()
