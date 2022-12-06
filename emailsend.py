import smtplib
import mimetypes  # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения
from email.mime.audio import MIMEAudio  # Аудио
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
import os


def send_email(addr_to, msg_subj, msg_text, files, URL, errors_):
    addr_from = "sasha.lorens@yandex.ru"  # Отправитель
    password = "LeNoVo_13572468"  # Пароль
    # URL = "https://drive.google.com/file/d/144XRAchdf6dioH13NK2FEkoVUwvss-zZ/view?usp=sharing"
    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = msg_subj  # Тема сообщения

    html = """ \
    <table border="0" cellpadding="0" cellspacing="0" style="margin:0; padding:0" width="100%">
    <tr>
      <td align="center">
        <center style="max-width: 600px; width: 100%;">
         <!--[if gte mso 9]>
  <table border="0" cellpadding="0" cellspacing="0" style="margin:0; padding:0"><tr><td>
  <![endif]-->
  <table border="0" cellpadding="0" cellspacing="0" style="margin:0px; padding:0px; text-align:center " width="100%"  bgcolor="#0044B0">
    <tr>
      <td>
          <!--[if gte mso 9]>
          <table border="0" cellpadding="0" cellspacing="0">
          <tr><td align="center">
                 <table border="0" cellpadding="0" cellspacing="0" width="300"     align="center"><tr><td>
          <![endif]-->
  
          <!-- Блок номер 1 -->
           <span style="display:inline-block; text-align: center; style="margin:10px 10px; padding:0px">
            <table border="0" cellpadding="0" cellspacing="0" style="margin:0px; padding:20px 10px 20px 10px" width="100%" bgcolor="#ffffff">
                <td>
                <img src="https://miem.hse.ru/mirror/pubs/share/direct/432333897.png" alt="" border="0" width="100%" height="150" style="display:block; padding: 0px; margin: auto"/>
            </table>
           </span>
          <!-- Блок номер 1 -->
   <!--[if gte mso 9]>
   </td></tr></table>
   </td>
   <td align="center">
   <table border="0" cellpadding="0" cellspacing="0" align="center"><tr><td>
   <![endif]-->
          <!-- Блок номер 2 -->
           <span style="display:inline-block; width:300px; text-align: center; font-family: 'arial' , sans-serif , 'helvetica' , sans-serif; font-size: 24px;  margin:30px 0px 0px 0px; padding:0; color: #ffffff;">
                Ваша прошивка
           </span>
          <!-- Блок номер 2 -->

           <!-- Блок номер 2 -->
           <span style="display:inline-block; width:300px; display:inline-block; width:300px; text-align: center; font-family: 'arial' , sans-serif , 'helvetica' , sans-serif; font-size: 24px; margin:30px 0px 30px 0px; padding:0; color: white;">
            <a  style="color:#ffffff" href=" """ + URL + """ ">Скачать</a>
            </span>
            <!-- Блок номер 2 -->

          <!--[if gte mso 9]>
          </td></tr></table>
          </td>
          </tr></table>
          <![endif]-->
              </td>
          </tr>
        </table>
      <!--[if gte mso 9]>
  </td></tr></table>
  <![endif]-->
       </center>   
      </td>
    </tr>
  </table>
    """

    html_error = """ \
    <table border="0" cellpadding="0" cellspacing="0" style="margin:0; padding:0" width="100%">
    <tr>
      <td align="center">
        <center style="max-width: 600px; width: 100%;">
         <!--[if gte mso 9]>
  <table border="0" cellpadding="0" cellspacing="0" style="margin:0; padding:0"><tr><td>
  <![endif]-->
  <table border="0" cellpadding="0" cellspacing="0" style="margin:0px; padding:0px; text-align:center " width="100%"  bgcolor="#0044B0">
    <tr>
      <td>
          <!--[if gte mso 9]>
          <table border="0" cellpadding="0" cellspacing="0">
          <tr><td align="center">
                 <table border="0" cellpadding="0" cellspacing="0" width="300"     align="center"><tr><td>
          <![endif]-->
  
          <!-- Блок номер 1 -->
           <span style="display:inline-block; text-align: center; style="margin:10px 10px; padding:0px">
            <table border="0" cellpadding="0" cellspacing="0" style="margin:0px; padding:20px 10px 20px 10px" width="100%" bgcolor="#ffffff">
                <td>
                <img src="https://miem.hse.ru/mirror/pubs/share/direct/432333897.png" alt="" border="0" width="100%" height="150" style="display:block; padding: 0px; margin: auto"/>
            </table>
           </span>
          <!-- Блок номер 1 -->
   <!--[if gte mso 9]>
   </td></tr></table>
   </td>
   <td align="center">
   <table border="0" cellpadding="0" cellspacing="0" align="center"><tr><td>
   <![endif]-->
          <!-- Блок номер 2 -->
           <span style="display:inline-block; width:300px; text-align: center; font-family: 'arial' , sans-serif , 'helvetica' , sans-serif; font-size: 24px;  margin:30px 0px 0px 0px; padding:0; color: #ffffff;">
                Ошибка
           </span>
          <!-- Блок номер 2 -->

           <!-- Блок номер 2 -->
           <span style="display:inline-block; width:300px; display:inline-block; width:300px; text-align: center; font-family: 'arial' , sans-serif , 'helvetica' , sans-serif; font-size: 24px; margin:30px 0px 30px 0px; padding:0; color: white;">
            <a  style="color:#ffffff" href=" """ + URL + """ ">Скачать</a>
            </span>
            <!-- Блок номер 2 -->

          <!--[if gte mso 9]>
          </td></tr></table>
          </td>
          </tr></table>
          <![endif]-->
              </td>
          </tr>
        </table>
      <!--[if gte mso 9]>
  </td></tr></table>
  <![endif]-->
       </center>   
      </td>
    </tr>
  </table>
    """

    body = msg_text  # Текст сообщения
    msg.attach(MIMEText(body, 'plain'))
    if errors_:
        msg.attach(MIMEText(html_error, 'html'))  # Добавляем в сообщение текст
    else:
        msg.attach(MIMEText(html, 'html'))  # Добавляем в сообщение текст

    process_attachement(msg, files)

    # ======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
    try:
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  # Создаем объект SMTP
        # server.starttls()                                  # Начинаем шифрованный обмен по TLS
        server.login(addr_from, password)  # Получаем доступ
        server.send_message(msg)  # Отправляем сообщение
        server.quit()  # Выходим

    except Exception as e:
        print(e)

    # ==========================================================================================================================


def process_attachement(msg, files):  # Функция по обработке списка, добавляемых к сообщению файлов
    for f in files:
        if os.path.isfile(f):  # Если файл существует
            attach_file(msg, f)  # Добавляем файл к сообщению
        elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)  # Получаем список файлов в папке
            for file in dir:
                # Перебираем все файлы и...
                attach_file(msg, f + "/" + file)
            # ...добавляем каждый файл к сообщению


def attach_file(msg, filepath):  # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)  # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:  # Если тип файла не определяется
        ctype = 'application/octet-stream'  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
    if maintype == 'text':  # Если текстовый файл
        with open(filepath) as fp:  # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
            fp.close()  # После использования файл обязательно нужно закрыть
    elif maintype == 'image':  # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':  # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:  # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
            file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
    msg.attach(file)  # Присоединяем файл к сообщению

# Использование функции send_email()

# send_email(addr_to="grisha.petuxov@mail.ru",  # "sasha.lorens@yandex.ru",
#                              msg_subj="Ваша прошивка",
#                              msg_text="Ваши файлы",
#                              files="",
#                              URL="")
#
