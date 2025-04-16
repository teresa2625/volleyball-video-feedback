from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import uuid
from video_utils import process_video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    temp_filename = f"temp_{uuid.uuid4().hex}.mp4"
    output_filename = f"output_{uuid.uuid4().hex}.avi"

    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_video(temp_filename, output_filename)

    return FileResponse(output_filename, media_type="video/x-msvideo")
