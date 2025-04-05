import sqlite3

# データベースファイル名
DATABASE_NAME = '履修登録.sqlite'

def create_department_table():
    """
    学科テーブルを作成し、初期データを登録する関数
    """

    # データベースに接続（ファイルが存在しない場合は作成される）
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # 学科テーブルを作成（存在しない場合のみ）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 学科 (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- IDは自動採番される主キー
            名前 VARCHAR NOT NULL                      -- 学科名は必須
        )
    ''')

    # 学科テーブルにデータを登録
    departments = [
        '経済学科',
        '心理学科',
        '機械学科',
        '生物学科',
        '情報学科',
    ]

    # データを挿入
    for name in departments:
        cursor.execute("INSERT INTO 学科 (名前) VALUES (?)", (name,))

    # 変更をコミット（データベースに反映）
    conn.commit()

    # データベース接続を閉じる
    conn.close()

    print("学科テーブルの作成とデータ登録が完了しました。")

# 関数を実行
if __name__ == "__main__":
    create_department_table()
