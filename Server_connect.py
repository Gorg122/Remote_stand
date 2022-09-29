import shutil
# import pymysql.cursors
#
# server = '127.0.0.1'
# database = 'doble'
# username = 'newuser'
# password = '12345'
#
# con = pymysql.connect(host='127.0.0.1',
#                       user='root',
#                       password='root',
#                       database='sakila',
#                       cursorclass=pymysql.cursors.DictCursor)
#
# with con:
#     cur = con.cursor()
#     cur.execute("SELECT VERSION()")
#
#     version = cur.fetchone()
#
#     print(version)
proj_dir = r"C:\PROJECT_930\Prototype_new_2\student_zip\grisha.petuxov"
shutil.make_archive("archive", 'zip', proj_dir)