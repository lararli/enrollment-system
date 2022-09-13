"""
This module implements a Session in an enrollment system given two files:
course data and user data.
"""

import json
from helpers import load
import os


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
        for course in courses.get('courses'):
            all_courses.append([course.get('course_id'), course.get('course_name'), course.get('workload')])
        return all_courses

    def course_details(self, course_id: int) -> dict:
        """
        List all information available about a course given the course_id.
        :param course_id: id of the course that the user want to see more information about.
        :return: returns a dictionary with courses data.
        """
        courses = load(self.course_data)
        course_info = {}
        for course in courses.get('courses'):
            if course.get('course_id') == course_id:
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
            for user in file_data.get('users'):
                if user.get('user_id') == user_id:
                    if course_id not in user.get('enrolled_courses'):
                        user.get('enrolled_courses').append(course_id)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                    else:
                        raise Exception('You are already enrolled in this course.')
        print('\nYou are now enrolled to this course!')

    @staticmethod
    def clear_screen():
        """
        Clear the screen in the terminal depending on the OS system.
        :return: function that clear the screen
        """
        return os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def menu() -> bool:
        """
        Returns a menu where the user can choose go back to the course list or exit the program.
        When the user choose go back, it returns True and when the users choose exit, it returns False.
        :return: True or False
        """
        print('What do you want to do now?')
        print('[0] Course List\n[1] Exit\n')
        choice = int(input('> '))
        if choice == 1:
            print('See you soon! =)')
            return False
        if choice == 0:
            return True
        else:
            raise Exception('Please, choose a valid option.')

    def show_all_courses(self) -> list:
        """
        Show all main information about courses stored in course_data file in a way that is readable for the user.
        """
        ids = []
        print('---------- COURSE LIST ----------\n')
        for course in self.list_all_courses():
            print(f'[{course[0]}] | {course[1]} | Workload: {course[2]} ')

    def show_course_details(self, course_id) -> dict:
        """
        Given a course id this method shows the information stored in the course_data file about the course in
        a way that is readable for the user.
        :return: return the item that contains information about the course.
        """
        print('---------- COURSE DETAILS ----------')
        course_list = self.course_details(course_id)
        for key in course_list.keys():
            print(f'\n{key.upper()}:')
            if isinstance(course_list.get(key), list):
                for value in course_list.get(key):
                    print(f'- {value}')
            else:
                print(course_list.get(key))
        return course_list

    def validate_if_course_exist(self, course_id: int) -> bool:
        """
        Validate if a course exist in course_data given a course_id
        If the course doesn't exist it'll raise a ValueError.
        """
        ids = []
        for course in self.list_all_courses():
            ids.append(course[0])
        if course_id in ids:
            return True
        raise ValueError('Please, choose a valid course id.')
