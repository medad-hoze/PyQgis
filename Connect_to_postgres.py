from psycopg2 import extensions

def CreateDBpostgreSQL(DB_NAME,user = 'postgres',password = '1515'):
    
    conn   = psycopg2.connect("dbname='' user={} password={}".format(user,password))

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level( autocommit )

    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE ' + str(DB_NAME))
    cursor.close()
    conn.close()
    print ('finish')

def connection(dbname,user = 'postgres',password = '1515'):
    conn   = psycopg2.connect("dbname={} user={} password={}".format(dbname,user,password))
    cursor = conn.cursor()
    return cursor,conn
    
def Connect_to_postgres(dbname,table,user = 'postgres',password = '1515'):
    
    cursor,conn = connection(dbname,user,password)
    cursor.execute("SELECT * from {}".format(table))

    record = cursor.fetchall()
    cursor.close()
    conn.close()
    return record


def List_to_SQLfields(schama):

    '''
    convert: [['id','bigint'],['title','varchar(128)'],['story','text'],['AGE','INT'],['INCOME','FLOAT']]
    to:      "(id bigint, title varchar(128), story text, AGE INT, SEX CHAR(1), INCOME FLOAT)"
    '''

    str_ = ''
    for i in schama: str_ = str_ + ', ' + ' '.join(n for n in i)
    return '(' + str_[2:] + ')'
    


def Check_if_table_exists(DBname,TBLname):
    cursor,conn = connection(DBname)
    cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", (TBLname,))
    ans = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    print (ans)
    return ans
    

def InsertDataToTable(DBname,TBLname,data,fields_list):

    #data        = [[1, 'Hussein'],[2, 'mohamad']]
    #fields_list = ['id', 'title']

    fields_str  = ', '.join(i for i in fields_list)
    data_str    = [str(tuple(j)) for j in data]

    cursor,conn = connection(DBname)

    for i in data_str: cursor.execute("insert into "+ TBLname +" ("+fields_str+") values "+ i +"")

    cursor.execute("select {} from {}".format(fields_str, TBLname))
    rows = cursor.fetchall()
    for r in rows:
        print (f"id {r[0]} name {r[1]}")
    conn.commit()
    cursor.close()
    conn.close()

def Create_Tale(DBname,TBLname,schama):

    schama = List_to_SQLfields(schama)

    cursor,conn = connection(DBname)
    cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", (TBLname,))
    ans = cursor.fetchone()[0]
    print(ans)
    if not ans:
        # cursor.execute("DROP TABLE IF EXISTS " +TBLname)
        cursor,conn = connection(DBname)
        sqlCreateTable = "create table "+TBLname+" {};".format(schama)
        cursor.execute(sqlCreateTable)
        conn.commit()
    cursor.close()
    conn.close()



#data = Connect_to_postgres(dbname = "Tel_aviv",table = "bshbldg")
#print (data)

#Check_if_table_exists("Tel_aviv","bshbldg")
#CreateDBpostgreSQL()

# schama = [['id','int'],['title','varchar(128)'],['story','text'],['AGE','INT'],['INCOME','FLOAT']]
# Create_Tale("Tel_aviv","NEWpythonaa")

# data        = [[1, 'Hussein'],[2, 'mohamad']]
# fields_list = ['id', 'title']
# InsertDataToTable("Tel_aviv","NEWpython",data,fields_list)



sql_stat = '''
select * 
from (
	select *, st_intersection(bshbldg.geom,tbl_stat1.geom)as geometry
	from bshbldg,(select * from bshstat where STAT_ID = 1) as tbl_stat1
	where st_intersects(bshbldg.geom,tbl_stat1.geom)
	) as newGeom
where geometry is not null
'''

cursor,conn = connection('Tel_aviv')

cursor.execute(sql_stat)
ans = cursor.fetchall()
for i in ans:
    print (i)


# sqlGetTableList = "SELECT table_schema,table_name FROM information_schema.tables where table_schema='test' ORDER BY table_schema,table_name ;"
# cursor.execute(sqlGetTableList)
# tables = cursor.fetchall()
# for table in tables:
#     print(table)

# cursor.close()
# conn.close()
