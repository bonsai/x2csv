import sqlite3
import os
import csv

DB_FILE = "your_database.db"  # 🔁 ここを対象のSQLiteファイル名に変更

def export_all_tables_to_csv(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # テーブル一覧を取得
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    if not tables:
        print("❌ テーブルが見つかりません。")
        return

    for table in tables:
        export_table_to_csv(cursor, table)

    conn.close()
    print("✅ 全テーブルのCSV出力が完了しました。")

def export_table_to_csv(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # カラム名取得
    column_names = [description[0] for description in cursor.description]

    filename = f"{table_name}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)
        writer.writerows(rows)

    print(f"✅ {table_name}.csv を出力しました。")

if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        print(f"❌ SQLiteファイルが見つかりません: {DB_FILE}")
    else:
        export_all_tables_to_csv(DB_FILE)
