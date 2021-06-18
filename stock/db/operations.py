from sqlalchemy.dialects.mysql import insert as __insert
from sqlalchemy import create_engine as __create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import mysql

from .base import Base
from ..models import *


def create_engine(connection_url):
    print('create new engine')
    engine = __create_engine(f'mysql+pymysql://{connection_url}',
                            pool_pre_ping=True,
                            pool_recycle=3600 * 7,
                            echo=False)
    # Amazon does not give you SUPER privileges on an RDS instance
    # (to prevent you from breaking things like replication accidentally).
    # To configure group_concat_max_len, use an RDS parameter group,
    # which allows you to configure a group of settings to apply to an instance.
    # https://stackoverflow.com/questions/31147206/amazon-rds-unable-to-execute-set-global-command
    try:
        engine.execute('SET GLOBAL max_allowed_packet=67108864;')
    except Exception as e:
        print(e)

    return engine


def create_all_tables_from_orm(engine):
    print('try to create tables:')
    for table in Base.metadata.sorted_tables:
        print(table)
    res = Base.metadata.create_all(engine)
    if res:
        print(f'create tables success: {res}')
    else:
        print('tables already exist')


def start_session(engine):
    print('==> start_session()')
    try:
        session = start_session.session_maker()
        session.execute("SELECT 1")
    except AttributeError:
        print('create new session maker')
        start_session.session_maker = sessionmaker()
        start_session.session_maker.configure(bind=engine)
        session = start_session.session_maker()
        session.execute('SELECT 1')
    return session


def compile_query(query):
    """from http://nicolascadou.com/blog/2014/01/printing-actual-sqlalchemy-queries"""
    compiler = query.compile if not hasattr(query, 'statement') else query.statement.compile
    return compiler(dialect=mysql.dialect())


def insert(session, model, _dict):
    table = model.__table__

    stmt = __insert(table).values(_dict)

    #print(compile_query(stmt))
    res = session.execute(stmt)
    #print(f'{res.rowcount} row(s) matched')
    return res.rowcount


def upsert(session, model, _dict):

    table = model.__table__

    _dict_wo_pk = dict(_dict)
    for pk in list(table.primary_key.columns):
        del _dict_wo_pk[pk.name]

    stmt = __insert(table).values(_dict)
    #print(f'dict = {_dict}, dict wo pk = {_dict_wo_pk}')
    upsert_stmt = stmt.on_duplicate_key_update(_dict_wo_pk)
    #print(compile_query(upsert_stmt))

    res = session.execute(upsert_stmt)
    #print(f'execute res: {res}')
    return res.rowcount


def delete_older_than(session, model, date_field, date_older_than):
    count = session.query(model).filter(date_field <= date_older_than).delete()
    return count


def count(session, model):
    return session.query(model).count()


def query_newer_than(session, model, date_field, date_newer_than):
    return session.query(model).filter(date_field >= date_newer_than)
