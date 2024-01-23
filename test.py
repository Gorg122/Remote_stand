import requests

url = 'http://127.0.0.1:8001/upload'
files = [('files', open('buttons.txt', 'rb')), ('files', open('JTAG_config.txt', 'rb')), ('files', open('video.mp4', 'rb'))]
# files = [('files', open('buttons.txt', 'rb')), ('files', open('JTAG_config.txt', 'rb'))]
resp = requests.post(url=url, files=files)
print(resp.json())