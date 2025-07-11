from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = FastAPI()

@app.post("/decode")
async def decode_qr(image: UploadFile = File(...)):
    contents = await image.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    decoded_objs = decode(img)
    if not decoded_objs:
        return JSONResponse(
            content={"success": False, "data": None, "message": "No QR code found"},
            status_code=400
        )

    results = [obj.data.decode('utf-8') for obj in decoded_objs]
    return {"success": True, "data": results}
