from datetime import timedelta

from fastapi import FastAPI, Request, Depends, status, Form, Response, HTTPException
from models import User, Course, Session
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

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    connection = Connection(user=credentials.get('user'),
                            pwd=credentials.get('password'),
                            db=credentials.get('database'),
                            host=credentials.get('host'))

    db = DB(connection)
    return db


def get_hashed_password(plain_password):
    return pwd_ctx.hash(plain_password)


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
    return RedirectResponse("/login")


manager.not_authenticated_exception = NotAuthenticatedException
app.add_exception_handler(NotAuthenticatedException, not_authenticated_exception_handler)


@app.get("/")
async def root():
    return {"Welcome to Hypathia!"}


@app.post("/login", status_code=status.HTTP_302_FOUND)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: DB = Depends(get_db)):
    user = await authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        return HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES)
    access_token = manager.create_access_token(
        data={"sub": user.get('email')},
        expires=access_token_expires
    )
    resp = RedirectResponse("/courses", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)
    return resp


@app.post("/user/{account_id}/deactivate")
async def deactivate_user(
        db=Depends(get_db),
        user=Depends(manager)
):
    account_id = user.get('account_id')
    return await db.deactivate_user(account_id)


@app.post("/course/{account_id}/deactivate")
async def deactivate_course(
        user=Depends(manager),
        db=Depends(get_db),
        course_id: int = None
):
    return await db.deactivate_course(course_id)


@app.get("/logout")
def logout(response: Response):
    response = RedirectResponse("/")
    manager.set_cookie(response, None)
    return response


@app.post("/register_course")
async def register_course(
        user=Depends(manager),
        db=Depends(get_db),
        name: str = Form(),
        workload: float = Form(),
        created_by: list = Form(),
        related_topics: list = Form()
):
    if 'admin' in user.get("account_role"):
        c = Course(
            name=name,
            workload=workload,
            created_by=created_by,
            related_topics=related_topics
        )
        await db.add_course(c.dict())
        return await db.search(table='course', column='name', value=name)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='You do not have access to create new courses.')


@app.get("/courses")
async def get_courses(db=Depends(get_db), user=Depends(manager)):
    return await db.search(table='course', column='active', value=True)


@app.post("/register")
async def register_user(
        db=Depends(get_db),
        first_name: str = Form(),
        last_name: str = Form(),
        email: str = Form(),
        password: str = Form(),
        account_role: list = Form()
):
    u = User(
        first_name=first_name,
        last_name=last_name, email=email,
        password=get_hashed_password(password),
        account_role=account_role
    )
    await db.add_user(u.dict())
    return await db.search(table='account', column='email', value=email)


# @app.post("/users")
# async def register_user(user: User):
#     await client.add_user(user.dict())
#     return "IT WORKEEEDDDD!!!!!!"


# @app.get("/courses")
# async def fetch_courses():
#     return await client.list_all_registers(table='courses')


# @app.post("/courses")
# async def register_course(course: Course):
#     await client.add_course(course.dict())
#     return "IT ALSO WORKEEEEEEEEED"


# @app.post("/courses/{course_id}/enroll")
# async def enroll(course_id: int, user_id: int, session_id: int, enrollment_id: int):
#     data = {'user_id': user_id, 'course_id': course_id, 'session_id': session_id, 'enrollment_id': enrollment_id}
#     res = await client.add_enrollments(data)
#     return res


# @app.get("/courses/{course_id}")
# async def search_course(course_id: UUID):
#     res = await client.search(table='courses', column='course_id', value=course_id)
#     return {"response": res, "status_code": status.HTTP_302_FOUND}


# @app.get("/users/{user_id}")
# async def search_user(user_id: UUID):
#     res = await client.search(table='users', column='user_id', value=user_id)
#     return {"response": res, "status_code": status.HTTP_302_FOUND}


# https://www.youtube.com/playlist?list=PLuhCJtW2i-wKK9HjfYJI4RIcd9AMIi88k
