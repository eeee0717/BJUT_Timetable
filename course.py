weekday_dict = {"星期一": 1, "星期二": 2, "星期三": 3, "星期四": 4, "星期五": 5, "星期六": 6, "星期日": 7}


class Course:
    name: str
    classroom: str
    weekday: int
    weeks: list[int]
    indexes: list[int]

    def __init__(self, name, classroom, weekday, weeks, indexes):
        self.name = name
        self.classroom = classroom
        self.weekday = weekday
        self.weeks = weeks
        self.indexes = indexes

    def __str__(self):
        return f"{self.name} {self.classroom} {self.weekday} {self.weeks} {self.indexes}"

    @staticmethod
    def week(start: int, end: int) -> list[int]:
        """
        返回周数列表：
        如 week(1, 3) -> [1, 2, 3]
        """
        return list(range(start, end + 1))

    @staticmethod
    def indexes(start: int, end: int) -> list[int]:
        """
        返回周数列表：
        如 indexes(1, 3) -> [1, 2, 3]
        """
        return list(range(start, end + 1))

    @staticmethod
    def get_course_name(text: str) -> str:
        name = ''.join(i for i in text.split('课程:')[1] if not i.isdigit())
        return name

    @staticmethod
    def get_course_classroom(text: str) -> str:
        classroom = text[1:-1]
        return classroom

    @staticmethod
    def get_course_week_info(text: str) -> list:
        start_week, end_week = map(int, text.split("周")[0].split("-"))
        weekday = weekday_dict[text.split(" ")[-1]]

        return [weekday, Course.week(start_week, end_week)]

    @staticmethod
    def get_course_indexes(text: str) -> list:
        sections = [s.strip() for s in text.split(',')]
        if not sections:
            return []

        time_slots = {
            "上": (0, 4),
            "下": (4, 8),
            "晚": (8, 12),
        }

        first_section = sections[0]
        time_key = first_section[0]  # 获取 "上", "下", "晚"
        start_index = time_slots.get(time_key)[0] + int(first_section[1:]) - 1
        end_index = start_index + len(sections) - 1

        return Course.indexes(start_index, end_index)
