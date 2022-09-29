import zipfile
#import resource
from resources import *
import contextlib

def file_zip_correct(file_path):
    try:
        archive = zipfile.ZipFile(file_path, 'r')
        archive.testzip()
        archive_list = archive.namelist()
        archive_name = str(archive)
        for itm in archive_list:
            if (itm.split('.')[1] == 'bat') or (itm.split('.')[1] == 'inf') or (itm.split('.')[1] == 'exe')\
                    or archive_name.endswith('.7z'):
                raise Exception()
        print('Все файлы соответсвуют безопастности')
        return 0, 'Все файлы соответсвуют безопастности'
    except zipfile.BadZipFile:
        print('Неправильный зип файл')
        return 1, 'Неправильный зип файл'
    except NameError:
        print('Нет такого файла')
        return 1, 'Нет такого файла'
    except Exception:
        print('Опасный файл')
        return 1, 'Опасный файл'


# @contextlib.contextmanager
# def limit(limit, type=resources.RLIMIT_AS):
#     soft_limit, hard_limit = resource.getrlimit(type)
#     resource.setrlimit(type, (limit, hard_limit)) # set soft limit
#     try:
#         yield
#     finally:
#         resource.setrlimit(type, (soft_limit, hard_limit)) # restore

#
# with limit(1 << 30): # 1GB
#     # 1GB  Здесь должна быть по идее разархивация файла
#     print('okey')

## STMP https://docs.python.org/3/library/smtplib.html проверка валидности почты
