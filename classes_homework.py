class Course:
    def __init__(self, name, start_date, number_of_lectures, teacher):
        self._name = name
        self._start_date = start_date
        self._number_of_lectures = number_of_lectures
        self._teacher = teacher
        self._lectures = []
        for lecture_number in range(number_of_lectures):
            lecture = Lecture(f'Lecture {lecture_number + 1}', lecture_number + 1, teacher)
            self._lectures.append(lecture)
            lecture.set_course(self)
        self._students = []
        self._homeworks = []

    def __str__(self):
        return f'{self._name} ({self._start_date})'

    def enrolled_by(self):
        return self._students

    @property
    def lectures(self):
        return self._lectures

    @property
    def number_of_lectures(self):
        return self._number_of_lectures

    @property
    def teacher(self):
        return self._teacher

    def enroll_student(self, enrolled_student):
        self._students.append(enrolled_student)

    def get_lecture(self, lecture_number):
        assert 0 < lecture_number <= self._number_of_lectures, 'Invalid lecture number'
        return self._lectures[lecture_number - 1]

    def get_homeworks(self):
        return self._homeworks

    def add_homework(self, homework):
        self._homeworks.append(homework)
        for hw_student in self._students:
            hw_student.assign_homework(homework)


class Lecture:
    def __init__(self, name, number, teacher):
        self._name = name
        self._number = number
        self._teacher = teacher
        self._teacher.add_lecture(self)
        self._homework = None
        self._course = None

    def set_course(self, course):
        self._course = course

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def number(self):
        return self._number

    @property
    def teacher(self):
        return self._teacher

    def get_homework(self):
        return self._homework

    def set_homework(self, homework):
        self._homework = homework
        homework.set_lecture(self)
        self._course.add_homework(homework)

    def new_teacher(self, teacher):
        self._teacher.remove_lecture(self)
        self._teacher = teacher
        self._teacher.add_lecture(self)


class Homework:
    def __init__(self, name, description):
        self._name = name
        self._description = description
        self._lecture = None
        self._students_done = {}

    def __str__(self):
        return f'{self._name}: {self._description}'

    def set_lecture(self, lecture):
        self._lecture = lecture

    def mark_done(self, hw_student):
        self._students_done[hw_student] = None
        self._lecture.teacher.add_homework(self)

    def done_by(self):
        return self._students_done

    def mark_homework(self, hw_student, hw_mark):
        self._students_done[hw_student] = hw_mark

    @property
    def students_done(self):
        return self._students_done


class Student:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name
        self._assigned_homeworks = []

    def __str__(self):
        return f'Student: {student.first_name} {student.last_name}'

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    def enroll(self, course):
        course.enroll_student(self)

    def assign_homework(self, homework):
        self._assigned_homeworks.append(homework)

    @property
    def assigned_homeworks(self):
        return self._assigned_homeworks

    def do_homework(self, homework):
        self._assigned_homeworks.remove(homework)
        homework.mark_done(self)


class Teacher:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name
        self._lectures = []
        self._homeworks_to_check = []
        self._checked_homeworks = {}

    def __str__(self):
        return f'Teacher: {self.first_name} {self.last_name}'

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    def add_lecture(self, lecture):
        self._lectures.append(lecture)

    def remove_lecture(self, lecture):
        self._lectures.remove(lecture)

    def teaching_lectures(self):
        return self._lectures

    @property
    def homeworks_to_check(self):
        return self._homeworks_to_check

    def add_homework(self, homework):
        self._homeworks_to_check.append(homework)

    def check_homework(self, homework, hw_student, hw_mark):
        assert 0 <= hw_mark <= 100, 'Invalid mark'
        if hw_student not in homework.students_done:
            raise ValueError('Student never did that homework')
        if homework.students_done[hw_student] is not None:
            raise ValueError('You already checked that homework')
        homework.mark_homework(hw_student, hw_mark)
        self._homeworks_to_check.remove(homework)
        self._checked_homeworks[hw_student] = homework


if __name__ == "__main__":
    main_teacher = Teacher('Thomas', 'Anderson')
    assert str(main_teacher) == f'Teacher: {main_teacher.first_name} {main_teacher.last_name}'

    python_basic = Course('Python basic', '31.10.2022', 16, main_teacher)
    assert len(python_basic.lectures) == python_basic.number_of_lectures
    assert str(python_basic) == 'Python basic (31.10.2022)'
    assert python_basic.teacher == main_teacher
    assert python_basic.enrolled_by() == []
    assert main_teacher.teaching_lectures() == python_basic.lectures

    students = [Student('John', 'Doe'), Student('Jane', 'Doe')]
    for student in students:
        assert str(student) == f'Student: {student.first_name} {student.last_name}'
        student.enroll(python_basic)

    assert python_basic.enrolled_by() == students

    third_lecture = python_basic.get_lecture(3)
    assert third_lecture.name == 'Lecture 3'
    assert third_lecture.number == 3
    assert third_lecture.teacher == main_teacher
    try:
        python_basic.get_lecture(17)
    except AssertionError as error:
        assert error.args == ('Invalid lecture number',)

    third_lecture.name = 'Logic separation. Functions'
    assert third_lecture.name == 'Logic separation. Functions'

    assert python_basic.get_homeworks() == []
    assert third_lecture.get_homework() is None
    functions_homework = Homework('Functions', 'what to do here')
    assert str(functions_homework) == 'Functions: what to do here'
    third_lecture.set_homework(functions_homework)

    assert python_basic.get_homeworks() == [functions_homework]
    assert third_lecture.get_homework() == functions_homework

    for student in students:
        assert student.assigned_homeworks == [functions_homework]

    assert main_teacher.homeworks_to_check == []
    students[0].do_homework(functions_homework)
    assert students[0].assigned_homeworks == []
    assert students[1].assigned_homeworks == [functions_homework]

    assert functions_homework.done_by() == {students[0]: None}
    assert main_teacher.homeworks_to_check == [functions_homework]

    for mark in (-1, 101):
        try:
            main_teacher.check_homework(functions_homework, students[0], mark)
        except AssertionError as error:
            assert error.args == ('Invalid mark',)

    main_teacher.check_homework(functions_homework, students[0], 100)
    assert main_teacher.homeworks_to_check == []
    assert functions_homework.done_by() == {students[0]: 100}

    try:
        main_teacher.check_homework(functions_homework, students[0], 100)
    except ValueError as error:
        assert error.args == ('You already checked that homework',)

    try:
        main_teacher.check_homework(functions_homework, students[1], 100)
    except ValueError as error:
        assert error.args == ('Student never did that homework',)

    substitute_teacher = Teacher('Agent', 'Smith')
    fourth_lecture = python_basic.get_lecture(4)
    assert fourth_lecture.teacher == main_teacher

    fourth_lecture.new_teacher(substitute_teacher)
    assert fourth_lecture.teacher == substitute_teacher
    assert len(main_teacher.teaching_lectures()) == python_basic.number_of_lectures - 1
    assert substitute_teacher.teaching_lectures() == [fourth_lecture]
    assert substitute_teacher.homeworks_to_check == []
