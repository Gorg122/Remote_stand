from fastapi import FastAPI
import requests
import httpx

app = FastAPI()

@app.get("/")
def root():
    return {'message': 'Welcome to GeeksforGeeks!'}


@app.get('/get_request')
def requests():
    api_url = "https://jsonplaceholder.typicode.com/users"
    all_files = requests.get(api_url).json()
    script = all_files[0]
    sof_file = all_files[1]
    return {'script': script, "sof_file": sof_file}

@app.post('/file')
def file_upload():
    url = "http://127.0.0.1:8000/file"
    files = {'buttons': open('buttons.txt', 'rb'),
             'log': open('JTAG_config.txt', 'rb'),
             'video': open('video.mp4', 'rb')}
    res = requests.post(url, files=files)
    if res.ok:
        print("It`s okay")
