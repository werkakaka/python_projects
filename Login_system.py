import hashlib

class AuthenticException(Exception):
    pass
class PermissionError(Exception):
    pass
class IncorrectPassword(AuthenticException):
    pass
class IncorrectUsername(AuthenticException):
    pass
class NotLoggedError(AuthenticException):
    pass
class PasswordTooShort(AuthenticException):
    pass
class UsernameAlreadyExists(AuthenticException):
    pass
class NotPermittedError(AuthenticException):
    pass

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.encrypt_password(password)
        self.is_logged = False

    def encrypt_password(self, password):
        return hashlib.sha256(f"{self.username}{password}".encode()).hexdigest()

    def check_password(self, password):
        return self.password == self.encrypt_password(password)

class Authenticator:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password):
        if username in self.users:
            raise UsernameAlreadyExists("Użytkownik już istnieje.")
        if len(password) < 8:
            raise PasswordTooShort("Hasło jest za krótkie.")
        self.users[username] = User(username, password)

    def login(self, username, password):
        if username not in self.users:
            raise IncorrectUsername("Podany użytkownik nie istnieje.")
        user = self.users[username]
        if not user.check_password(password):
            raise IncorrectPassword("Błędne hasło.")
        user.is_logged = True
        return True

    def is_logged_in(self, username):
        return self.users.get(username, None) and self.users[username].is_logged

class Authorizor:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}

    def add_permission(self, permission):
        if permission in self.permissions:
            raise PermissionError("To uprawnienie już istnieje.")
        self.permissions[permission] = set()

    def permit_user(self, username, permission):
        if permission not in self.permissions:
            raise PermissionError("Nie ma takiego uprawnienia.")
        if username not in self.authenticator.users:
            raise IncorrectUsername("Nieprawidłowa nazwa użytkownika.")
        self.permissions[permission].add(username)

    def check_permission(self, username, permission):
        if permission not in self.permissions:
            raise PermissionError("Nie ma takiego uprawnienia.")
        if username not in self.authenticator.users:
            raise IncorrectUsername("Nieprawidłowa nazwa użytkownika.")
        if username not in self.permissions[permission]:
            raise NotPermittedError("Użytkownik nie ma dostępu do tego uprawnienia.")
        if not self.authenticator.is_logged_in(username):
            raise NotLoggedError("Użytkownik nie jest zalogowany.")
        return True

authenticator = Authenticator()
authorizor = Authorizor(authenticator)

class Editor:
    def __init__(self):
        self.username = None
        self.options = {
            "a": self.login,
            "b": self.test,
            "c": self.change,
            "d": self.quit
        }

    def login(self):
        username = input("Podaj nazwę użytkownika: ")
        password = input("Podaj hasło: ")
        try:
            authenticator.login(username, password)
            self.username = username
            print("Zalogowano pomyślnie.")
        except AuthenticException as e:
            print(f"Błąd: {e}")

    def is_permitted(self, permission):
        try:
            return authorizor.check_permission(self.username, permission)
        except AuthenticException as e:
            print(f"Błąd: {e}")
            return False

    def test(self):
        if self.is_permitted("testowanie"):
            print("Testowanie programu...")

    def change(self):
        if self.is_permitted("edytowanie"):
            print("Edytowanie programu...")

    def quit(self):
        print("Kończenie działania programu.")
        exit()

    def run(self):
        while True:
            print("\nMenu:")
            print("a) Zaloguj się")
            print("b) Testuj program")
            print("c) Edytuj program")
            print("d) Wyjdź")
            choice = input("Wybierz opcję: ")
            action = self.options.get(choice)
            if action:
                action()
            else:
                print("Niepoprawna opcja.")

authenticator.add_user("admin", "supersecurepassword")
authenticator.add_user("tester", "testpassword1")

authorizor.add_permission("testowanie")
authorizor.add_permission("edytowanie")

authorizor.permit_user("tester", "testowanie")
authorizor.permit_user("admin", "testowanie")
authorizor.permit_user("admin", "edytowanie")

editor = Editor()
editor.run()
