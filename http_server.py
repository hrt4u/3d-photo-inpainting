import uuid

import aiofiles
import aiofiles.os
from fastapi import FastAPI, UploadFile, HTTPException
from starlette.responses import FileResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/animate_mock/")
async def animate_mock(file: UploadFile):
    if file.content_type != "image/jpeg":
        raise HTTPException(400, detail="Invalid image type")

    session_dirname = uuid.uuid4().hex
    session_filename = f"{uuid.uuid4().hex}.jpg"
    await aiofiles.os.makedirs(f'image/{session_dirname}', exist_ok=True)

    async with aiofiles.open(f'image/{session_dirname}/{session_filename}', 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return FileResponse("video/moon_circle.mp4", media_type="video/mp4", filename="result.mp4")


@app.post("/animate/")
async def animate(file: UploadFile):
    from main import go_magic

    if file.content_type != "image/jpeg":
        raise HTTPException(400, detail="Invalid image type")

    session_dirname = uuid.uuid4().hex
    session_filename = f"{uuid.uuid4().hex}.jpg"
    await aiofiles.os.makedirs(f'image/{session_dirname}', exist_ok=True)
    await aiofiles.os.makedirs(f'video/{session_dirname}', exist_ok=True)

    async with aiofiles.open(f'image/{session_dirname}/{session_filename}', 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    go_magic("argument.yml", src_folder=f"image/{session_dirname}", video_folder=f"video/{session_dirname}")

    return FileResponse(f"video/{session_dirname}", media_type="video/mp4", filename="result.mp4")
