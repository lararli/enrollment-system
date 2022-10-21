from datetime import timedelta
from fastapi import FastAPI, Depends, status, Form, Response, HTTPException, Query
from models import User, Course, Role
from credentials import credentials
from postgres.db import Connection, DB
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse


app = FastAPI()

ACCESS_TOKEN_EXPIRES = 60
SECRET_KEY = credentials.get('secret_key')
manager = LoginManager(SECRET_KEY, token_url='/login', use_cookie=True)
manager.cookie_name = 'auth'

pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    connection = Connection(user=credentials.get('user'),
                            pwd=credentials.get('password'),
                            db=credentials.get('database'),
                            host=credentials.get('host'))

    db = DB(connection)
    return db


def get_hashed_password(plain_password):
    return str(pwd_ctx.hash(plain_password))


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_ctx.verify(plain_password, hashed_password)


@manager.user_loader()
async def get_user(email: str, db=get_db()):
    resp = await db.search(table='account', column='email', value=email)
    return resp


async def authenticate_user(email: str, password: str, db=Depends(get_db)):
    user = await db.search(table='account', column='email', value=email)
    if user is None:
        return None
    if not verify_password(plain_password=password, hashed_password=user.get('hashed_password')):
        return None
    if user.get('active') is False:
        return None
    return user


class NotAuthenticatedException(Exception):
    pass


def not_authenticated_exception_handler(request, exception):
    return RedirectResponse('/login')


manager.not_authenticated_exception = NotAuthenticatedException
app.add_exception_handler(NotAuthenticatedException, not_authenticated_exception_handler)


@app.get('/')
async def root():
    return {'Welcome to Hypathia!'}


@app.post('/login')
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = await authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if user is None:
        return HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES)
    access_token = manager.create_access_token(
        data={'sub': user.get('email')},
        expires=access_token_expires
    )
    resp = RedirectResponse('/courses', status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)
    return resp


@app.get('/logout')
def logout(response: Response, db=Depends(get_db)):
    response = RedirectResponse('/')
    manager.set_cookie(response, None)
    return response


@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(
        db=Depends(get_db),
        first_name: str = Form(),
        last_name: str = Form(),
        email: str = Form(),
        password: str = Form(),
        account_role: Role = Form()
):
    u = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=get_hashed_password(password),
        account_role=account_role
    )

    await db.add_user(u.dict())
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)


@app.put('/user/{account_id}/deactivate', status_code=status.HTTP_200_OK)
async def deactivate_user(
        db=Depends(get_db),
        user=Depends(manager)
):
    account_id = user.get('account_id')
    await db.deactivate_user(account_id)
    return RedirectResponse('/', status_code=status.HTTP_200_OK)


@app.post('/register_course', status_code=status.HTTP_201_CREATED)
async def register_course(
        user=Depends(manager),
        db=Depends(get_db),
        name: str = Form(),
        workload: float = Form(),
        created_by: list = Form(),
        related_topics: list = Form()
):
    # check if the course already exist
    if 'admin' in user.get('account_role'):
        c = Course(
            name=name,
            workload=workload,
            created_by=created_by,
            related_topics=related_topics
        )
        await db.add_course(c.dict())
        return {'Course successfully created!'}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='You do not have access to create new courses.')


@app.put('/course/{course_id}/deactivate')
async def deactivate_course(
        user=Depends(manager),
        db=Depends(get_db),
        course_id: int = None
):
    if 'admin' in user.get('account_role'):
        await db.deactivate_course(course_id)
        return {'Course successfully deleted!'}
    return HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Unauthorized operation.')


@app.get('/courses', status_code=status.HTTP_200_OK)
async def get_courses(db=Depends(get_db), user=Depends(manager)):
    return await db.search(table='course', column='active', value=True)


@app.post('/courses/{course_id}/enroll', status_code=status.HTTP_201_CREATED)
async def enroll(db=Depends(get_db), user=Depends(manager), course_id: int = None):
    list_enrolled_courses = await db.search(table='enrollment', column='account_id', value=user.get('account_id'))

    if list_enrolled_courses is not None:
        for course in list_enrolled_courses:
            if course.get('course_id') == course_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='You are already enrolled to this course'
                )
    await db.enroll_user(account_id=user.get('account_id'), course_id=course_id)
    return {'Congratulations! You give the first step for a bright future!'}


@app.get('/user/{account_id}/enrolled_courses', status_code=status.HTTP_200_OK)
async def enrollments(db=Depends(get_db), user=Depends(manager)):
    enrolled_courses = await db.search(table='enrollment', column='account_id', value=user.get('account_id'))

    if enrolled_courses is None:
        return {'You are not enrolled to any course yet.'}

    ids = []
    for enrolled_course in enrolled_courses:
        ids.append(enrolled_course.get('course_id'))

    courses_info = []
    for value in ids:
        course = await db.search(table='course', column='course_id', value=value)
        courses_info.append(course[0])

    return courses_info


@app.delete('/user/{user_id}/permanently-delete')
async def permanently_delete_user(db=Depends(get_db), user=Depends(manager)):
    await db.delete_enrollment(value=user.get('account_id'))
    await db.delete_user(value=user.get('account_id'))
    return RedirectResponse('/logout')

