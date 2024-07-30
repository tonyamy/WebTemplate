from typing import List, Type, Dict, Any

from sqlalchemy import asc, desc
from sqlalchemy.orm import scoped_session


class ModelCrud:
    def __init__(self, Session: Type[scoped_session], Model):
        self.session = Session
        self.Model = Model

    def paginate_query(
            self,
            filters=None,
            page: int = 1,
            page_size: int = 10,
            sort_by: str = None,
            sort_order: str = 'asc'
    ) -> Dict[List[any], int]:
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

    def create(self, data: Dict[str, Any]) -> Any:
        """
        创建新记录
        :param data: 数据字典
        :return: 创建的记录
        """
        instance = self.Model(**data)
        self.session.add(instance=instance)
        self.session.commit()
        return instance

    def read(self, record_id: Any) -> Any:
        """
        读取单个记录
        :param record_id: 记录ID
        :return: 查询的记录
        """
        return self.session.query(self.Model).get(record_id)

    def update(self, record_id: Any, data: Dict[str, Any]) -> Any:
        """
        更新记录
        :param record_id: 记录ID
        :param data: 更新的数据字典
        :return: 更新的记录
        """
        instance = self.session.query(self.Model).get(record_id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            self.session.commit()
        return instance

    def delete(self, record_id: Any) -> bool:
        """
        删除记录
        :param record_id: 记录ID
        :return: 是否成功删除
        """
        instance = self.session.query(self.Model).get(record_id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False
