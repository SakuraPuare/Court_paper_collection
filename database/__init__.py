from typing import Union, Any, Type

import pymysql

from config import config


class Tables:
    name = ''
    keys = []
    types = []
    description = ''

    def __init__(self) -> None:
        pass

    @property
    def key(self) -> str:
        return ', '.join(self.keys)

    @property
    def type(self) -> str:
        return ', \n'.join([' '.join(i) for i in self.types])

    @staticmethod
    def value(data: Any, with_bracket: bool = True) -> str:
        if isinstance(data, tuple) or len(data) == 1:
            data = data[0]
            return f"""( {', '.join([f'"{i}"' for i in data.to_list()])} )"""
        elif isinstance(data, list) and len(data) > 1:
            return ', \n'.join([f"""( {', '.join([f'"{j}"' for j in i.to_list()])} )""" for i in data])


class PaperList(Tables):
    name = 'paper_list'
    keys = ['name', 'location', 'url', 'description', 'case_number', 'date', 'type']
    types = [
        ("id", "int", "auto_increment", "PRIMARY KEY", "comment 'id'"),
        ("name", "varchar(256)", "comment '文书名称'"),
        ("location", "varchar(128)", "comment '地点'"),
        ("url", "varchar(512)", "comment '文书链接'"),
        ("description", "text", "comment '文书描述'"),
        ("case_number", "varchar(128)", "comment '案号'"),
        ("date", "date", "comment '时间'"),
        ("type", "varchar(32)", "comment '案件类型'"),
    ]
    description = '文书列表'

    def __init__(self) -> None:
        super().__init__()


class SQL:
    def __init__(self, host: str = config.host, user: str = config.username, password: str = config.password,
                 dbname: str = config.dbname, charset: str = 'utf8mb4') -> None:
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname

        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, charset=charset)
        self.cursor = self.db.cursor()
        try:
            self._execute("USE `{}`;".format(self.dbname))
        except pymysql.OperationalError as e:
            if e.args[0] == 1049:
                self.init()

    def _execute(self, sql: str, args: tuple = ()) -> Union[tuple, None]:
        self.cursor.execute(sql, args)
        try:
            self.db.commit()
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            self.db.rollback()
            print(e)
            return None

    def init(self) -> None:
        self._execute(
            "CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".format(config.dbname))
        self._execute("USE `{}`;".format(config.dbname))

        # 初始化 paper_list 表
        paper_list = PaperList()
        self._execute(
            f"create table if not exists `{paper_list.name}` ({paper_list.type}) comment '{PaperList.description}';")

    def insert_into(self, table: str, types: Type[Tables], data: Any) -> Union[tuple, None]:
        types = types()
        key = types.key
        data = types.value(data)
        sql = f"""insert into `{table}` ({key}) values {data};"""
        return self._execute(sql)


if __name__ == '__main__':
    sql = SQL()
    resp = sql._execute("select * from information_schema.SCHEMATA where SCHEMA_NAME = 'test';")
    pass
