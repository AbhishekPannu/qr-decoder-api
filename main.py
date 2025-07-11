import os
import numpy as np
import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.post("/decode")
async def decode_qr(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        npimg = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if not data:
            return JSONResponse(
                content={"success": False, "data": None, "message": "No QR code found"},
                status_code=400
            )

        return {"success": True, "data": [data]}
    
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"Error: {str(e)}"},
            status_code=500
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use dynamic port from Railway or 8000 locally
    uvicorn.run("main:app", host="0.0.0.0", port=port)
