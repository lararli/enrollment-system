from helpers import create_id
import json


class Courses:

    def __init__(self, file):
        self.file = file
        self.course_id = None

    def add_course(self, course_name: str, related_topics: list, created_by: list, work_load: float, content: list):
        """
        :TODO: add a validation if already exist.
        """
        self.course_id = create_id(self.file, 'courses', 'course_id')
        new_course = {
            "course_id": 1,
            "course_name": course_name,
            "related_topics": related_topics,
            "created_by": created_by,
            "workload": work_load,
            "content": content
        }
        with open(self.file, "r+") as file:
            file_data = json.load(file)
            file_data['courses'].append(new_course)
            file.seek(0)
            json.dump(file_data, file, indent=4)


