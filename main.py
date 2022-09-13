from user import User
from session import Session


def main(courses: str, users: str, init: bool = True):
    u = User(user_data=users)
    session = Session(course_data=courses, user_data=users)

    if u.credentials():

        while init:
            session.clear_screen()
            all_courses = session.show_all_courses()
            course_id = int(input('Choose a course:\n> '))

            if course_id in all_courses:
                session.clear_screen()
                session.show_course_details(course_id)
                user_choice = input('> ').lower()
                if user_choice == 'y':
                    try:
                        session.associate_user_to_course(u.user_id, course_id)
                    except Exception as e:
                        print(e)
                    finally:
                        init = session.menu()
                elif user_choice == 'n':
                    init = session.menu()
                else:
                    try:
                        raise Exception('This is not a valid option.')
                    except Exception as e:
                        print(e)
                        init = session.menu()
            else:
                raise Exception('This is not a valid option.')


if __name__ == '__main__':
    main(courses='data/course_data.json', users='data/user_data.json')
