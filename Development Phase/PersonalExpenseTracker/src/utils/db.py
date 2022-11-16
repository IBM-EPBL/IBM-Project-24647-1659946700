from ibm_db import connect, tables, fetch_assoc, exec_immediate, execute
import ibm_db_dbi


def Results(command):
    ret = []
    result = fetch_assoc(command)

    while result:
        ret.append(result)
        result = fetch_assoc(command)
    
    return 
    
def ExecuteDB(command):
    try:
        conn = ibm_db_dbi.Connection(Connection)
        cur = conn.cursor()

        cur.execute(command)
        result = cur.fetchall()
        print(result)
        return result, True
    except ibm_db_dbi.ProgrammingError as e:
        print(e)
        return [], True
    except Exception as e:
        print(e)
        return None, False


def ConnectDB(dsn_db, dsn_hostname, dsn_password, dsn_port, dsn_protocol, dsn_uid, dsn_driver):
    global Connection
    dsn = (
        "DRIVER={0};"
        "DATABASE={1};"
        "HOSTNAME={2};"
        "PORT={3};"
        "PROTOCOL={4};"
        "UID={5};"
        "PWD={6};"
    ).format(dsn_driver, dsn_db, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_password)
    # print(dsn)
    try:
        Connection = connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=sbw89798;PWD=HJt8K2gcWfmXEawR;", "", "")
        print("Database Connected Successfully!!!")
    except Exception as e:
        print("Unable to Connect to Database!")
        print(e)