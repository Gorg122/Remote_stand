import pymysql.cursors
def connect():
    con = pymysql.connect(host='DESKTOP-CG9VKI4',
                          port=3306,
                          user='user_1',
                          password='user_1',
                          database='labstandstatus',
                          cursorclass=pymysql.cursors.DictCursor)
    return con

def status_check(con):  ############# Функция  проверки статуса и выставления ################
    with con:
        cur = con.cursor()
        cur.execute("SELECT id FROM status WHERE status = 3")
        answer = cur.fetchall()
        print(answer)
        clear_for_work_stand = answer[0]['id']
        print(clear_for_work_stand)
        try:
            clear_for_work_stand = answer[0]['id']
            print(clear_for_work_stand)
        except:
            print("На данный момент свободных стендов нет")
    return clear_for_work_stand

con = connect()
clear_for_work_stand = status_check(con)
print(clear_for_work_stand)
