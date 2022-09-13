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

    def __init__(self, user_data: str):
        self.user_data = user_data
        self.login = None
        self.password = None
        self.user_id = None

    # @property
    # def login(self):
    #     return self._login
    #
    # @login.setter
    # def login(self, login):
    #     """
    #     Validate if the login provided by the user has digits, spaces or is empty.
    #     Raises an exception if does.
    #     :param login: parameter provided by the getter.
    #     """
    #     if any(ch.isdigit() for ch in login) or len(login.strip()) == 0 or ' ' in login:
    #         raise Exception('The login can not contain spaces or digits!')
    #     self._login = login.lower()

    def validate_credentials(self) -> bool:
        """
        Validate if the user credentials assigned in the initialization exist in the user_data file.
        Raises an exception in case of the login exist but the password is different.
        :return: True if the credentials are right,
        False if the credentials doesn't exist in the file.
        """
        users_list = load(self.user_data)
        for item in users_list.get('users'):
            if self.login == item.get('login') and self.password == item.get('password'):
                self.user_id = item.get('user_id')
                print("Welcome again!")
                return True
            if self.login == item.get('login') and self.password != item.get('password'):
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
            file_data.get('users').append(new_user)
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
        for user in file_data.get('users'):
            if user.get('user_id') == self.user_id:
                list_index.append(index)
            index += 1
        for i in list_index:
            del file_data.get('users')[i]
        with open(self.user_data, 'w') as file:
            json.dump(file_data, file, indent=4)

    def credentials(self):
        def login_validation(attempts: int = 4):
            """
            Asks the user the login and password, validate if the login doesn't contain
            digits or spaces or is not empty, and raises an exception if contains.
            If the login pass in the validation, it'll validate the credentials using the validate_credentials
            method and will create a user if the validation returns False.
            This method use a recursive function to give, as standard, 5 attempts to the user put the
            correct password or a login that fit the initial requirements.
            If the user don't do it in the attempts, the program is going to raise an Exception and the user will
            need to reinitialize the session.
            """
            self.login = str(input('Login:\n> '))
            self.password = str(input('Password:\n> '))

            if any(ch.isdigit() for ch in self.login) or len(self.login.strip()) == 0 or ' ' in self.login:
                raise Exception('The login can not contain spaces or digits!')
            self.login = self.login.lower()

            try:
                # user = User(user_data=self.user_data)
                if not self.validate_credentials():
                    self.create_user()
            except Exception as e:
                print(e)
                assert attempts < 0 or int(attempts) == attempts, 'Please, choose a integer positive number.'
                if attempts == 0:
                    raise Exception('You exceeded the number of attempts. Reinitialize the session.')
                return login_validation(attempts - 1)
            else:
                return True

        return login_validation()

    @staticmethod
    def user_choice():
        """
        Asks the user if they want to enroll to a course.
        And if the user input a value that is not Y or N, it'll
        raise an exception, otherwise it'll return the input of the user itself.
        :return: the input itself.
        """
        print('\nDo you want to enroll to this course? [Y/N]')
        choice = input('> ').lower()
        if choice not in ['y', 'n']:
            raise ValueError('Please, choose between Y or N.')
        return choice.lower()
