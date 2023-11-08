import json
from sqlalchemy import create_engine, and_, desc
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload
from datetime import datetime, timedelta

from model import CustomJSONEncoder, Discount, Question

# 创建数据库引擎，替换 'mysql+mysqlconnector' 为你的 MySQL 配置
engine = create_engine('mysql+pymysql://root:lilinze1@localhost/douban')


def save_question(question: Question):
    # 创建一个会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 添加 Question 对象到会话
    session.add(question)

    # 提交会话以将数据保存到数据库
    session.commit()
    session.close()


def save_questions(questions: list):
    # 创建一个会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 添加 Question 对象到会话
    session.add_all(questions)

    # 提交会话以将数据保存到数据库
    session.commit()
    session.close()


def get_question(title, type):
    # 创建一个会话
    Session = sessionmaker(bind=engine)
    session = Session()
    question = session.query(Question).filter(
        Question.title == title and Question.type == type).first()
    session.close()
    return question


def get_all_questions(type):
    # 创建一个会话
    Session = sessionmaker(bind=engine)
    session = Session()
    three_days_ago = datetime.now() - timedelta(days=3)
    and_condition = and_(
        Question.type == type,
        Question.create_time >= three_days_ago
    )
    questions = session.query(Question).filter(and_condition).options(
        subqueryload(Question.discounts)).order_by(desc(Question.create_time)).limit(100).all()

    for question in questions:
        # 显式加载关联的 Discount 对象
        question.discounts  # 这将触发关联对象的加载
        for discount in question.discounts:
            # 重新附加 Discount 对象到会话
            session.add(discount)  # 重新附加 Discount 到会话

    session.close()
    return questions


if __name__ == '__main__':
    questions = get_all_questions('cat')
    print(json.dumps(questions, cls=CustomJSONEncoder))
