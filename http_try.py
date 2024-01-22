from fastapi import FastAPI
import requests
import httpx
import uvicorn

# app = FastAPI()

# @app.get("/")
# def root():
#     return {'message': 'Welcome to GeeksforGeeks!'}


# @app.get('/get_request')
def request():
    api_url = "https://postman-echo.com/get"
    response = requests.get(api_url)
    print(response.status_code)
    # script = all_files[0]
    # sof_file = all_files[1]
    # return {'script': script, "sof_file": sof_file}

# @app.post('/file')
def file_upload():
    # url = "http://127.0.0.1:8000/file"
    url = 'https://postman-echo.com/post'
    files = {'buttons': open('buttons.txt', 'rb'),
             'log': open('JTAG_config.txt', 'rb'),
             'video': open('video.mp4', 'rb')}
    res = httpx.post(url, files=files)
    print(res.status_code)
    # if res.ok:
    #     print("It`s okay")
if __name__ == "__main__":
    # request()
    file_upload()
    # file_upload()
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
