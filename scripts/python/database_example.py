import sqlite3
from sqlite3 import OperationalError

WSI_TABLE = "wsi_table"
RECIEVE_TIME_COL = "received_time"
REPORT_TIME_COL = "report_time"
SERIAL_COL = "serial_number"
REPORT_TYPE_COL = "report_type"
report_columns = (RECIEVE_TIME_COL, REPORT_TIME_COL, REPORT_TYPE_COL, SERIAL_COL)

#define datbase schema file
dbfile = "my_database.db"


def execute_sql(command):
    with sqlite3.connect(dbfile, check_same_thread=False) as conn:  # DECLARE CONNECTION AT START OF WITH BLOCK
        try:
            cur = conn.cursor()
            cur.execute(command)
            conn.commit()
            print("Executed SQL: " + command)
        except OperationalError as e:
            print("Exception executing: " + command)
            print("OperationalError: " + str(e.args))
            return "sqlite3 operational error: " + str(e)
        except Exception as e:
            print("Exception executing: " + command)
            print("Exception: " + str(e))
            return "sqlite3 error: " + str(e)

    return cur



#Create Table
createWsiTable = ("CREATE TABLE " + WSI_TABLE + "("
                              "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                              RECIEVE_TIME_COL + " DATE, " +
                              REPORT_TIME_COL + " DATE, " +
                              REPORT_TYPE_COL + " VARCHAR(10), " +
                              SERIAL_COL+ " VARCHAR(20) " +
                              ");")
execute_sql(createWsiTable)

#Insert 2 records
columns = ",".join(report_columns)
values = "1500399262," + \
         "4500399262," + \
         "'TURBULANCE'," + \
         "'DR1234501'"
insertRecord = "INSERT INTO {table} ({cols}) VALUES ({vals})".format(table=WSI_TABLE, cols=columns, vals=values)
execute_sql(insertRecord)
execute_sql(insertRecord)


#Query database
sql_query = "SELECT {cols} FROM {table} ORDER BY id DESC LIMIT 1".format(cols=columns, table=WSI_TABLE)
#sql_query = "SELECT * FROM {table} ".format(table=WSI_TABLE, cols=columns, vals=values)
#sql_query = "SELECT Count(*) FROM {table} ".format(table=WSI_TABLE, cols=columns, vals=values)
cursor = execute_sql(sql_query)

#Read result
# See here for details: https://docs.python.org/2/library/sqlite3.html
print ("curson is type: " + str(type(cursor)))

# If there are multiple rows and you want to get them all run this to get a list of tuples:
#  fetched_value = cursor.fetchall()
#  print ("fetchall() return type: " + str(type(fetched_value)))
#
# or for one row at a time:
fetched_value = cursor.fetchone()
print ("fetchone() return type: " + str(type(fetched_value)))

d = {}
for i in range(len(fetched_value)):
    if isinstance(fetched_value[i], unicode):
        value = fetched_value[i].encode('ascii', 'replace')
    else:
        value = fetched_value[i]
    d[report_columns[i]] = value

print ("Dictionary of column/values: {}".format(d))
