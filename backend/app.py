from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import uuid
from video_process import processor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("✅ Top-level print works", flush=True)
logger.info("✅ Top-level logger works")

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    logger.info("🚀 Inside route - logger works")
    print("🖨️ Inside route - print works", flush=True)
    temp_filename = f"temp_{uuid.uuid4().hex}.mp4"
    output_filename = f"output_{uuid.uuid4().hex}.mp4"

    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    processor.process_video(temp_filename, output_filename)

    return FileResponse(output_filename, media_type="video/mp4")
