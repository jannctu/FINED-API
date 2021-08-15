import numpy as np
import time
from PIL import Image
import requests
import io
import os
import sys
import gc 
import torch

import uvicorn
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from fastapi import FastAPI, Request, UploadFile, File, HTTPException,status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.modules.fined.inference_api import get_FINED_edge
import cv2

#os.environ["CUDA_VISIBLE_DEVICES"]="0"

app = FastAPI(title='FINED Edge Detection')
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
        CORSMiddleware,
        allow_origins= ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# @app.on_event("startup")
# async def startup_event():
#     os.environ["CUDA_VISIBLE_DEVICES"]="0"

# @app.on_event("shutdown")
# def shutdown_event():
#     torch.cuda.empty_cache()

#route

@app.get('/',response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.post("/predict/image")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image must be jpg or png format!")

    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    timestr = time.strftime("%Y%m%d-%H%M%S")

    prediction = get_FINED_edge(img,timestr)
    res, im_png = cv2.imencode(".png", prediction)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

@app.get("/predict/url")
async def predict_url(img_url):
    extension = img_url.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image must be jpg or png format!")

    im = Image.open(requests.get(img_url, stream=True).raw)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    open_cv_image = np.array(im.convert('RGB')) 
    
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    prediction = get_FINED_edge(open_cv_image,timestr)
    res, im_png = cv2.imencode(".png", prediction)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0",port=8000)