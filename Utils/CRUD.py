from typing import List, Type, Dict

from sqlalchemy import asc, desc
from sqlalchemy.orm import scoped_session

from Models.DbAccount import Base
from Utils.Utils import auto_convert_to_dict


class ModelCrud:
    def __init__(self, Session: Type[scoped_session], Model):
        self.session = Session
        self.Model = Model

    @auto_convert_to_dict
    def getById(self, modelId: int, id: int, ):  # 使用泛型 T 来指定返回值类型
        return self.session.query(self.Model).filter_by(modelId == id).first()

    def insert(self, model):
        return self.session.add(model)

    def delById(self, modelId: int, id: int):
        return self.session.query(self.Model).filter_by(modelId == id).delete()

    @auto_convert_to_dict
    def paginate_query(
            self,
            filters=None,
            page: int = 1,
            page_size: int = 10,
            sort_by: str = None,
            sort_order: str = 'asc'
    ) -> Dict[List[Base], int]:
        """
        分页查询函数
        :param filters: 查询条件列表
        :param page: 当前页码
        :param page_size: 每页大小
        :param sort_by: 排序字段
        :param sort_order: 排序顺序 ('asc' 或 'desc')
        :return: 查询结果列表，总记录数
        """

        if filters is None:
            filters = []
        query = self.session.query(self.Model)

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
