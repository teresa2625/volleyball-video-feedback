from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uuid
import json
import os
from video_process import processor
from starlette.background import BackgroundTasks

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

def cleanup(temp_file):
    os.unlink(temp_file)

@app.post("/upload/")
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    bbox: str = Form(...),
):
    video_id = uuid.uuid4().hex
    input_path = f"input_{video_id}.mp4"
    output_path = f"output_{video_id}.mp4"

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    box = json.loads(bbox)
    processor.process_video(input_path, output_path, box)
    background_tasks.add_task(cleanup, input_path)
    background_tasks.add_task(cleanup, output_path)

    return FileResponse(output_path, media_type="video/mp4", filename=os.path.basename(output_path))

@app.get("/feedback/")
async def get_feedback(background_tasks: BackgroundTasks, filename: str):
    feedback_file = filename.replace(".mp4", "_feedback.csv")
    if not os.path.exists(feedback_file):
        return JSONResponse(content={"feedback": "No feedback found."})
    with open(feedback_file) as f:
        background_tasks.add_task(cleanup, feedback_file)
        return JSONResponse(content={"feedback": f.read()})
