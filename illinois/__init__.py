# Where: illinois/__init__.py

## Why:
## if you are not able to install: pip install mysqlclient, then use this:
## That line makes Django think “oh, this is MySQLdb” even though it’s PyMySQL.

# Add:

import pymysql
pymysql.install_as_MySQLdb()

