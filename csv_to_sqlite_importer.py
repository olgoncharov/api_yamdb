import sqlite3

import pandas


def main():

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    tables = [ "api_genre", "api_category", "api_title", "api_review", "api_comment"]
    csv_files = [ "genre.csv", "category.csv", "genre_title.csv", "review.csv", "comments.csv"]
    index = 0

    for filename in csv_files:
        filepath = f'data/{filename}'
        with open(filepath) as f:
            f = pandas.read_csv(filepath)
            f.to_sql(tables[index], conn, if_exists='append', index=False)
            index += 1

    # Проверка
    for table in tables:
        cursor.execute(f"SELECT * FROM {table} LIMIT 36")
        table_content = cursor.fetchall()
        print(table)
        print(table_content)

    conn.close()


if __name__ == "__main__":
    main()
