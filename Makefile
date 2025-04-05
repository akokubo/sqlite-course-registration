履修登録.sqlite: create_departments.py create_users.py create_courses.py create_grades.py
	python create_departments.py
	python create_users.py
	python create_departments.py
	python create_courses.py 
	python create_grades.py
	
clean:
	rm -f *.sqlite
