"""Run the SQL healthcare analytics project with an in-memory SQLite database."""

from pathlib import Path
import sqlite3


PROJECT_DIR = Path(__file__).resolve().parent


def split_queries(sql_text):
    blocks = []
    current_title = "SQL analysis"
    current_sql = []

    for line in sql_text.splitlines():
        if line.startswith("-- "):
            if current_sql:
                blocks.append((current_title, "\n".join(current_sql).strip()))
                current_sql = []
            current_title = line[3:].strip()
        else:
            current_sql.append(line)

    if current_sql:
        blocks.append((current_title, "\n".join(current_sql).strip()))

    return [(title, query) for title, query in blocks if query]


def print_results(cursor, title, query):
    print(f"\n{title}")
    print("-" * len(title))
    cursor.execute(query)
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]
    print(" | ".join(headers))
    print("-+-".join("-" * len(header) for header in headers))
    for row in rows:
        print(" | ".join(str(value) for value in row))


def main():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    cursor.executescript((PROJECT_DIR / "schema.sql").read_text())
    cursor.executescript((PROJECT_DIR / "seed_data.sql").read_text())

    query_text = (PROJECT_DIR / "analysis_queries.sql").read_text()
    for title, query in split_queries(query_text):
        print_results(cursor, title, query)

    connection.close()


if __name__ == "__main__":
    main()
