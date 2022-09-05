"""
This module implements the creation of
new users and the validation of existent users.
"""
import json
from helpers import load, create_id


class User:
    """
    This class implements the user object, where all the objects will have a login, password
    and a user id that will be assigned after validation.
    """

    def __init__(self, login: str, password: str, user_data: str):
        self.login = login
        self.password = password
        self.user_data = user_data
        self.user_id = None

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, login):
        """
        Validate if the login provided by the user has digits, spaces or is empty.
        Raises an exception if does.
        :param login: parameter provided by the getter.
        """
        if any(ch.isdigit() for ch in login) or len(login.strip()) == 0 or ' ' in login:
            raise Exception('The login can not contain spaces or digits!')
        self._login = login.lower()

    def validate_credentials(self) -> bool:
        """
        Validate if the user credentials assigned in the initialization exist in the user_data file.
        Raises an exception in case of the login exist but the password is different.
        :return: True if the credentials are right,
        False if the credentials doesn't exist in the file.
        """
        users_list = load(self.user_data)
        for item in users_list.get("users"):
            if self.login == item['login'] and self.password == item['password']:
                self.user_id = item['user_id']
                print("Welcome again!")
                return True
            if self.login == item['login'] and self.password != item['password']:
                raise Exception('The password you specified are not correct! Please, try again.')
        return False

    def create_user(self) -> None:
        """
        Create a new user with the login and password assigned in the object initialization,
        assign a unique user_id and store it in the user_data file.
        """
        self.user_id = create_id(self.user_data, 'users', 'user_id')
        new_user = {
            'user_id': self.user_id,
            'login': self.login,
            'password': self.password,
            'enrolled_courses': []
        }
        with open(self.user_data, "r+") as file:
            file_data = json.load(file)
            file_data['users'].append(new_user)
            file.seek(0)
            json.dump(file_data, file, indent=4)
        print('A new user has been created! Welcome! =)')

    def delete_user(self) -> None:
        """
        Delete the register stored in the user_data file that refers to the User object.
        """
        index = 0
        list_index = []
        file_data = load(self.user_data)
        for user in file_data['users']:
            if user['user_id'] == self.user_id:
                list_index.append(index)
            index += 1
        for i in list_index:
            del file_data['users'][i]
        with open(self.user_data, 'w') as file:
            json.dump(file_data, file, indent=4)
