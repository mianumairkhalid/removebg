from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import io

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # or restrict to ["http://localhost:5500"]
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    # Read uploaded image into memory
    input_bytes = await file.read()
    img = Image.open(io.BytesIO(input_bytes)).convert("RGBA")
    
    # Remove background
    result = remove(img)
    
    # Prepare PNG buffer
    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)
    
    # Return as image/png streaming response
    return StreamingResponse(buffer, media_type="image/png")
