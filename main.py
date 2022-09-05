from helpers import clear_screen
from user import User
from session import Session


def credentials(user_data: str):
    def login_validation(attempts: int = 4):
        login = str(input('Login:\n> '))
        password = str(input('Password:\n> '))
        try:
            user = User(login=login, password=password, user_data=user_data)
            if not user.validate_credentials():
                user.create_user()
        except Exception as e:
            print(e)
            assert attempts < 0 or int(attempts) == attempts, 'Please, choose a integer positive number.'
            if attempts == 0:
                raise Exception('You exceeded the number of attempts. Reinitialize the session.')
            return login_validation(attempts - 1)
        else:
            return user
    return login_validation()


def show_all_courses(all_courses: list):
    ids = []
    print('---------- COURSE LIST ----------\n')
    for course in all_courses:
        print(f'[{course[0]}] | {course[1]} | Workload: {course[2]} ')
        ids.append(course[0])
    return ids


def show_course_details(course_list: dict):
    print('---------- COURSE DETAILS ----------')
    for key in course_list.keys():
        print(f'\n{key.upper()}:')
        if type(course_list[key]) is list:
            for value in course_list[key]:
                print(f'- {value}')
        else:
            print(course_list[key])
    return course_list


def option_menu():
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


def main(courses: str, users: str, session_init: bool = True):
    u1 = credentials(users)
    session = Session(course_data=courses, user_data=users)

    while session_init:
        clear_screen()
        all_courses = show_all_courses(session.list_all_courses())
        course_id = int(input('Choose a course:\n> '))

        if course_id in all_courses:
            clear_screen()
            show_course_details(session.course_details(course_id))
            print('\nDo you want to enroll to this course? [Y/N]')
            user_choice = input('> ').lower()
            if user_choice == 'y':
                try:
                    session.associate_user_to_course(u1.user_id, course_id)
                    print('\nYou are now enrolled to this course!')
                except Exception as e:
                    print(e)
                finally:
                    session_init = option_menu()
            elif user_choice == 'n':
                session_init = option_menu()
            else:
                raise Exception('This is not a valid option.')
        else:
            raise Exception('This is not a valid option.')


if __name__ == '__main__':
    main(courses='data/course_data.json', users='data/user_data.json')
