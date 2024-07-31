from Models.User import User
from Service.Engine import session_scope
from Utils.Utils import log_exceptions


@log_exceptions
def userLogin(username: str, password: str):
    with session_scope() as session:
        user_info: User = session.query(User).filter(User.username == username).filter(
            User.password == password).first()
        result = user_info.to_dict()
    return result

# print(userLogin("admin", '123123'))
