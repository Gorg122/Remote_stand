from fastapi import File, UploadFile, FastAPI
from typing import List
import uvicorn
import os
app = FastAPI()
@app.post("/upload")
def upload(files: List[UploadFile] = File(...)):
    for file in files:
        try:
            try:
                os.mkdir("files")
                print(os.getcwd())
            except Exception as e:
                print(e)
            file_name = os.getcwd() + "/files/" + file.filename.replace(" ", "-")
            with open(file_name, 'wb+') as f:
                f.write(file.file.read())
                f.close()
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()

    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

# @app.post("/create_file/")
# async def image(image: UploadFile = File(...)):
#     print(image.file)
#     # print('../'+os.path.isdir(os.getcwd()+"images"),"*************")
#     try:
#         os.mkdir("images")
#         print(os.getcwd())
#     except Exception as e:
#         print(e)
#     file_name = os.getcwd()+"/images/"+image.filename.replace(" ", "-")
#     with open(file_name,'wb+') as f:
#         f.write(image.file.read())
#         f.close()
#    file = jsonable_encoder({"imagePath":file_name})
#    new_image = await add_image(file)
#    return {"filename": new_image}