from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json

Base = declarative_base()


class Discount(Base):
    __tablename__ = 'discounts'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey(
        'questions.id'), nullable=False)  # 外键
    content = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)

    def __init__(self, content, answer):
        self.content = content
        self.answer = answer


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    link = Column(String(255))
    type = Column(String(10))
    create_time = Column(DateTime, default=datetime.now)

    # 定义一对多关系，一个问题可以有多个折扣
    discounts = relationship('Discount', backref='question', lazy='subquery')

    def __init__(self, title, link, type, create_time):
        self.title = title
        self.link = link
        self.type = type
        self.create_time = create_time

    def set_discounts(self, discounts: list):
        self.discounts = discounts

    def add_discount(self, discount: Discount):
        self.discounts.append(discount)

    def get_discounts(self) -> list:
        return self.discounts


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Question):
            # 如果是 Question 对象，将其转化为可序列化的字典
            return {
                'id': obj.id,
                'title': obj.title,
                'link': obj.link,
                'create_time': obj.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'discounts': [
                    {
                        'id': discount.id,
                        'question_id': discount.question_id,
                        'question': discount.content,
                        'answer': discount.answer
                    }
                    for discount in obj.discounts
                ]
            }
        return super().default(obj)


if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://root:lilinze1@localhost/douban')
    Base.metadata.create_all(engine)
