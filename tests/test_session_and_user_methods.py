from helpers import load
from user import User
from session import Session
from pytest import fixture

user_data = 'user_data_example.json'
course_data = 'course_data_example.json'


@fixture
def user():
    resp = User(login='ciclano.silva', password=12345, user_data=user_data)
    return resp


@fixture
def session():
    resp = Session(user_data=user_data, course_data=course_data)
    return resp


def test_validate_credentials_if_doesnt_exist(user):
    if user.validate_credentials():
        user.delete_user()
    assert user.validate_credentials() is False
    user.delete_user()


def test_validate_credentials_if_exist(user):
    if not user.validate_credentials():
        user.create_user()
    assert user.validate_credentials() is True


def test_create_user_that_doesnt_exist(user):
    if user.validate_credentials():
        user.delete_user()
    assert user.validate_credentials() is False
    user.create_user()
    assert user.validate_credentials() is True
    user.delete_user()


def test_delete_user(user):
    if not user.validate_credentials():
        user.create_user()
    assert user.validate_credentials() is True
    user.delete_user()
    assert user.validate_credentials() is False


def test_list_all_courses(session):
    file = load(course_data)
    all_courses = []
    for course in file['courses']:
        all_courses.append([course['course_id'], course['course_name'], course['workload']])
    resp = session.list_all_courses()
    assert all_courses == resp


def test_course_details(session):
    file = load(course_data)
    courses = file['courses']
    assert session.course_details(courses[0]['course_id']) == courses[0]


def test_associate_user_to_course(user, session):
    course_id = 5
    file = load(user_data)
    users = file['users']
    for item in users:
        print(item)
        if item['user_id'] == user.user_id:
            print(item['user_id'])
            assert course_id in item['enrolled_courses'] is False
            session.associate_user_to_course(user_id=user.user_id, course_id=course_id)
            assert course_id in item['enrolled_courses'] is True
    user.delete_user()
