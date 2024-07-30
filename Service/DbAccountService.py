from Models.DbAccount import DbAccount
from Service.Engine import session_scope
from Utils.CRUD import ModelCrud

with session_scope() as session:
    data, total = ModelCrud(session, DbAccount).paginate_query()
    print([i.to_dict() for i in data])
