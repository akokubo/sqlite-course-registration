import sqlite3
import random

DATABASE_FILE = "履修登録.sqlite"
grades_pool = ['S', 'A', 'B', 'C', 'D']

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# 成績テーブルが存在しなければ作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS 成績 (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    学生ID INTEGER REFERENCES 学生(ID),
    科目ID INTEGER REFERENCES 科目(ID),
    成績 CHAR(1)
);
''')

# 学生一覧（学生ID, 学科ID）
cursor.execute("SELECT ID, 学科ID FROM 学生")
students = cursor.fetchall()

# 科目一覧（科目ID, 学科ID）→ 学科ごとに分けて保存（ID順＝簡単）
cursor.execute("SELECT ID, 学科ID FROM 科目 ORDER BY 学科ID, ID")
courses = cursor.fetchall()

courses_by_dept = {}
for course_id, dept_id in courses:
    courses_by_dept.setdefault(dept_id, []).append(course_id)

grades_data = []

for student_id, dept_id in students:
    dept_courses = courses_by_dept.get(dept_id, [])
    if len(dept_courses) < 22:
        continue  # 科目数が少なすぎる場合はスキップ

    # --- 過去に取得済みの科目（成績あり） ---
    num_past_courses = random.randint(12, 20)

    # 簡単な科目が選ばれやすいように重みを設定
    weights = [1.0 / (i + 1) for i in range(len(dept_courses))]
    past_courses = random.choices(dept_courses, weights=weights, k=num_past_courses)
    past_courses = list(dict.fromkeys(past_courses))[:num_past_courses]
    past_courses.sort()

    for i, course_id in enumerate(past_courses):
        # 簡単な科目ほど良い成績を取りやすい
        diff_ratio = i / (len(past_courses) - 1) if len(past_courses) > 1 else 0
        probs = [max(0.0, 1.0 - diff_ratio * (j / 4)) for j in range(5)]
        total = sum(probs)
        probs = [p / total for p in probs]
        grade = random.choices(grades_pool, weights=probs, k=1)[0]

        grades_data.append((student_id, course_id, grade))

    # --- 現在履修中の科目（成績なし） ---
    remaining_courses = list(set(dept_courses) - set(past_courses))
    weights = [1.0 / (i + 1) for i in range(len(remaining_courses))]
    current_courses = random.choices(remaining_courses, weights=weights, k=10)
    current_courses = list(dict.fromkeys(current_courses))[:10]

    for course_id in current_courses:
        grades_data.append((student_id, course_id, None))  # 成績なし

# INSERT（成績が None の場合はNULLになる）
cursor.executemany("INSERT INTO 成績 (学生ID, 科目ID, 成績) VALUES (?, ?, ?)", grades_data)

conn.commit()
conn.close()

print(f"{len(grades_data)} 件の成績データを投入しました（成績なしも含む）。")
