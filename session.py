"""
This module implements a Session in an enrollment system given two files:
course data and user data.
"""

import json
from helpers import load


class Session:
    """
    This class implements a session, where all the objects will have as
    attributes the path containing both information about courses and users.
    """
    def __init__(self, course_data: str, user_data: str):
        self.course_data = course_data
        self.user_data = user_data

    def list_all_courses(self) -> list:
        """
        List all main information about courses given the attribute course_data.
        :return: Return a list with the course_id, course_name and course_workload.
        """
        all_courses = []
        courses = load(self.course_data)
        for course in courses['courses']:
            all_courses.append([course['course_id'], course['course_name'], course['workload']])
        return all_courses

    def course_details(self, course_id: int) -> dict:
        """
        List all information available about a course given the course_id.
        :param course_id: id of the course that the user want to see more information about.
        :return: returns a dictionary with courses data.
        """
        courses = load(self.course_data)
        course_info = {}
        for course in courses['courses']:
            if course['course_id'] == course_id:
                course_info.update(course)
        return course_info

    def associate_user_to_course(self, user_id: int, course_id: int) -> None:
        """
        Associates the user in a course given the user_id and course_id.
        It adds the course id in the user_data.json file.
        :param user_id: id of the user that wants to be associated in a course
        :param course_id: id of the course that the wants to be associated with.
        """
        with open(self.user_data, "r+") as file:
            file_data = json.load(file)
            for user in file_data['users']:
                if user['user_id'] == user_id:
                    if course_id not in user['enrolled_courses']:
                        user['enrolled_courses'].append(course_id)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                    else:
                        raise Exception('You are already enrolled in this course.')
