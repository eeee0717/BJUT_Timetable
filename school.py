from datetime import timedelta, datetime
from hashlib import md5

from course import Course


class School:
    duration: int = 45
    timetable: list[tuple[int, int]] = [
        (8, 00),
        (8, 50),
        (9, 55),
        (10, 45),
        (13, 30),
        (14, 20),
        (15, 25),
        (16, 15),
        (18, 00),
        (18, 50),
        (19, 55),
        (20, 45),
    ]
    start: tuple[int, int, int]
    courses: list[Course]
    start_dt: datetime
    HEADERS = [
        "BEGIN:VCALENDAR",
        "METHOD:PUBLISH",
        "VERSION:2.0",
        "X-WR-CALNAME:课表",
        "X-WR-TIMEZONE:Asia/Shanghai",
        "CALSCALE:GREGORIAN",
        "BEGIN:VTIMEZONE",
        "TZID:Asia/Shanghai",
        "END:VTIMEZONE"]
    FOOTERS = ["END:VCALENDAR"]

    def __init__(self, start, courses):
        self.start = start
        self.start_dt = datetime(*self.start[:3])
        self.start_dt -= timedelta(days=self.start_dt.weekday())
        self.courses = courses

    def time(self, week: int, weekday: int, index: int, plus: bool = False) -> datetime:
        """
        生成详细的日期和时间：
        week: 第几周，weekday: 周几，index: 第几节课，plus: 是否增加课程时间
        """
        date = self.start_dt + timedelta(weeks=week - 1, days=weekday - 1)
        return date.replace(
            hour=self.timetable[index][0], minute=self.timetable[index][1]
        ) + timedelta(minutes=self.duration if plus else 0)

    def generate(self) -> str:
        runtime = datetime.now()
        texts = []
        courses = [
            [
                "BEGIN:VEVENT",
                f"SUMMARY:{course.name}-{course.classroom}",
                f"DTSTART;TZID=Asia/Shanghai:{self.time(week, course.weekday, course.indexes[0]):%Y%m%dT%H%M%S}",
                f"DTEND;TZID=Asia/Shanghai:{self.time(week, course.weekday, course.indexes[-1], True):%Y%m%dT%H%M%S}",
                f"DTSTAMP:{runtime:%Y%m%dT%H%M%SZ}",
                f"UID:{md5(str((course.name, week, course.weekday,course.indexes[0])).encode()).hexdigest()}",
                f"URL;VALUE=URI:",
                "END:VEVENT",
            ]
            for course in self.courses
            for week in course.weeks
        ]
        items = [i for j in courses for i in j]
        for line in self.HEADERS + items + self.FOOTERS:
            first = True
            while line:
                texts.append((" " if not first else "") + line[:72])
                line = line[72:]
                first = False
        return "\n".join(texts)
