from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
import base64
import numpy as np
import cv2
import torch
from detect_plate import detect_Recognition_plate, load_model, init_model

app = FastAPI()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

detect_model = load_model("weights/plate_detect.pt", device)
plate_rec_model = init_model(device, "weights/plate_rec_color.pth", is_color=True)


class ImageBase64(BaseModel):
    image: str


@app.post("/predict-plate")
async def predict_plate(image_base64: ImageBase64):
    try:
        image_data = base64.b64decode(image_base64.image)
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 检查图像是否有效
        if img is None:
            return {"code": 400, "msg": "image error", "data": []}

        # 处理四通道图片（如果有）
        if img.shape[-1] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # 调用车牌识别函数
        dict_list = detect_Recognition_plate(
            model=detect_model,
            orgimg=img,
            device=device,
            plate_rec_model=plate_rec_model,
            img_size=640,
            is_color=True
        )

        dict_list = [convert_dict(item) for item in dict_list]

        return {"code": 200, "msg": "success", "data": dict_list}

    except Exception as e:
        return {"code": 500, "msg": f"error: {str(e)}", "data": []}


@app.post("/predict-plate-by-file")
async def predict_plate_by_file(file: UploadFile):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 检查图像是否有效
        if img is None:
            return {"code": 400, "msg": "image error", "data": []}

        # 处理四通道图片（如果有）
        if img.shape[-1] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # 调用车牌识别函数
        dict_list = detect_Recognition_plate(
            model=detect_model,
            orgimg=img,
            device=device,
            plate_rec_model=plate_rec_model,
            img_size=640,
            is_color=True
        )

        dict_list = [convert_dict(item) for item in dict_list]

        return {"code": 200, "msg": "success", "data": dict_list}

    except Exception as e:
        return {"code": 500, "msg": f"error: {str(e)}", "data": []}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


def convert_numpy(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    return obj


def convert_dict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = convert_dict(v)
        elif isinstance(v, list):
            d[k] = [convert_numpy(i) if not isinstance(i, dict) else convert_dict(i) for i in v]
        else:
            d[k] = convert_numpy(v)
    return d
