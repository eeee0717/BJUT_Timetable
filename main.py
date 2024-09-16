import sys
import docx
from docx import Document
from course import Course
from school import School
import os


def read_docx(doc: Document) -> str:
    text = ""
    for table in doc.tables:
        for row in table.rows[1:]:
            for cell in row.cells[2:]:
                if cell.text is None or cell.text == '':
                    continue
                text += cell.text + '\n'
    return text


def split_course_info(course: str) -> Course:
    course_info = course.split('\n')
    name = Course.get_course_name(course_info[0])
    classroom = Course.get_course_classroom(course_info[2])
    weekday, weeks = Course.get_course_week_info(course_info[3])
    indexes = Course.get_course_indexes(course_info[4])
    course = Course(name, classroom, weekday, weeks, indexes)
    return course


def main():
    print("1. 请将课表.doc转换成课表.docx")
    print("2. 填写课表.docx路径")
    print("3. 填写开学第一周的时间")

    while True:
        docx_path = input("课表.docx路径：")
        if os.path.exists(docx_path) and docx_path.endswith('.docx'):
            break
        else:
            print("文件不存在或不是.docx格式，请重新输入。")

    while True:
        start_date = input("开学第一周时间（格式：2024,9,2）：")
        try:
            year, month, day = map(int, start_date.split(','))
            start = (year, month, day)
            break
        except:
            print("输入格式错误，请重新输入。")

    doc = docx.Document(docx_path)
    text = read_docx(doc)

    courses = text.split('课程')
    courses = list(set(filter(lambda x: x != '', courses)))
    courses = ['课程' + course for course in courses]
    course_list = []
    for course in courses:
        course_list.append(split_course_info(course))
    school = School(start=start, courses=course_list)
    try:
        output_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "课表.ics")  # 使用可执行文件的目录
        with open(output_path, "w") as w:
            w.write(school.generate())
        print(f"课表.ics文件已生成在：{output_path}")
    except Exception as e:
        print(f"生成文件时出错: {e}")
    input("按任意键退出...")  # 等待用户输入


if __name__ == '__main__':
    main()
