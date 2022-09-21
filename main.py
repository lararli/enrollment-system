from user import User
from session import Session
from fastapi import FastAPI, Query


def main(courses: str, users: str, init: bool = True):
    u = User(user_data=users)

    if u.credentials():
        session = Session(course_data=courses, user_data=users)

        while init:
            session.clear_screen()
            session.show_all_courses()
            course_id = int(input('Choose a course:\n> '))

            try:
                session.validate_if_course_exist(course_id)
                session.clear_screen()
                session.show_course_details(course_id)
                resp = u.user_choice()
                if resp == 'y':
                    session.associate_user_to_course(u.user_id, course_id)
            except Exception as e:
                print(e)
            finally:
                init = session.menu()


if __name__ == '__main__':
    main(courses='data/course_data.json', users='data/user_data.json')
