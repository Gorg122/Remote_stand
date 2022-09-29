import os
chek = 1
User_path_to_file = "student_zip/Desorder2881488"
users_dir = "C:/PROJECT_930/Prototype_new_2/" + User_path_to_file
os.chdir(users_dir)
print(users_dir, '\n')
print(users_dir, '\n')
for files in os.listdir(users_dir):
    if files.endswith("errors.txt"):
        check = open(files)
        chek1 = check.read(2)
        er_name = files
        check.close()
        print(chek1,'\n')

    print('\n')
    if files.endswith("Proj_compilation.txt"):
        check = open(files)
        chek2 = check.read(2)
        log_name = files
        check.close()
        print(chek2,'\n')
if chek2 == "": #and os.path.exists(users_dir + "" + log_name):
        os.remove(users_dir + "/" + log_name)
if chek1 == "" and os.path.exists(users_dir + "" + er_name):
        os.remove(users_dir + "/" + er_name)