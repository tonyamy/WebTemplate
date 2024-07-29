from typing import Any, List, Tuple, Type

from sqlalchemy import desc, asc
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session


# 创建一个基类
@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def paginate_query(
        session: Session,
        model: Type[Base],
        filters: List[Any] = [],
        page: int = 1,
        page_size: int = 10,
        sort_by: str = None,
        sort_order: str = 'asc'
) -> Tuple[List[Base], int]:
    """
    分页查询函数

    :param session: SQLAlchemy Session
    :param model: 数据库模型类
    :param filters: 查询条件列表
    :param page: 当前页码
    :param page_size: 每页大小
    :param sort_by: 排序字段
    :param sort_order: 排序顺序 ('asc' 或 'desc')
    :return: 查询结果列表，总记录数
    """

    query = session.query(model)

    # 应用过滤条件
    for condition in filters:
        query = query.filter(condition)

    # 获取总记录数
    total_count = query.count()

    # 应用排序
    if sort_by:
        if sort_order == 'asc':
            query = query.order_by(asc(sort_by))
        else:
            query = query.order_by(desc(sort_by))

    # 应用分页
    query = query.offset((page - 1) * page_size).limit(page_size)

    # 执行查询
    results = query.all()

    return results, total_count
