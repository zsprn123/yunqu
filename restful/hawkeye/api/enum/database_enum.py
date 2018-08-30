# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/enum/database_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 477 bytes
from enum import Enum

class Driver(Enum):
    mysql = 'com.mysql.jdbc.Driver'
    oracle = 'oracle.jdbc.driver.OracleDriver'
    db2 = 'com.ibm.db2.jcc.DB2Driver'
    sqlserver = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
    informix = 'com.informix.jdbc.IfxDriver'
    postgres = 'org.postgresql.Driver'


class DatabaseType(Enum):
    MYSQL = 'mysql'
    ORACLE = 'oracle'
    DB2 = 'db2'
    SQLSERVER = 'sqlserver'
    INFORMIX = 'informix'
    POSTGRES = 'postgres'
# okay decompiling ./restful/hawkeye/api/enum/database_enum.pyc
