import numpy as np
import cv2
from pyzbar.pyzbar import decode
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/decode")
async def decode_qr(image: UploadFile = File(...)):
    try:
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

    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"Error: {str(e)}"},
            status_code=500
        )
