import os
import cv2
import numpy as np
import base64
import io
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO

app = FastAPI(
    title="Vehicle Detection API", 
    description="AI-powered vehicle classification & detection API using YOLOv8."
)

# Set directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# YOLOv8 Model Variable
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        # Load the pretrained nano model (downloaded automatically if not cached)
        model = YOLO("yolov8n.pt")
        print("YOLOv8 Nano model loaded successfully.")
    except Exception as e:
        print(f"Error loading YOLOv8 model: {e}")

@app.get("/")
def read_root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse(
        """
        <html>
            <head><title>Vehicle Detection</title></head>
            <body style="font-family: sans-serif; text-align: center; padding: 50px; background-color: #0f172a; color: #f8fafc;">
                <h1>Vehicle Model Detection System</h1>
                <p>System is starting up. Static files are not yet fully generated.</p>
            </body>
        </html>
        """
    )

@app.post("/api/detect")
async def detect_vehicles(file: UploadFile = File(...)):
    global model
    if model is None:
        raise HTTPException(status_code=503, detail="YOLO Model is not loaded yet. Please try again in a few seconds.")
    content_type = file.content_type
    if not content_type:
        import mimetypes
        content_type, _ = mimetypes.guess_type(file.filename or "")
        if not content_type:
            content_type = "application/octet-stream"
            
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")
    
    try:
        # Read uploaded image bytes
        contents = await file.read()
        
        # Decode image using PIL (which supports webp, transparent pngs, etc. robustly)
        try:
            pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")
            
        h, w, _ = img.shape
        
        # Run inference
        # Classes: 2: car, 3: motorcycle, 5: bus, 7: truck
        results = model(img, classes=[2, 3, 5, 7])
        
        detections = []
        annotated_img = img.copy()
        
        # BGR Values to match CSS Hex:
        # Rose CSS: rgb(244, 63, 94) -> BGR: (94, 63, 244)
        # Emerald CSS: rgb(16, 185, 129) -> BGR: (129, 185, 16)
        # Amber CSS: rgb(245, 158, 11) -> BGR: (11, 158, 245)
        # Blue CSS: rgb(59, 130, 246) -> BGR: (246, 130, 59)
        bgr_colors = {
            "car": (94, 63, 244),
            "motorcycle": (129, 185, 16),
            "bus": (11, 158, 245),
            "truck": (246, 130, 59)
        }
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                
                detections.append({
                    "class": cls_name,
                    "confidence": conf,
                    "box": [round(x1), round(y1), round(x2), round(y2)]
                })
                
                # Draw on annotated image
                color = bgr_colors.get(cls_name, (241, 102, 99)) # Fallback color
                
                # Draw box border
                cv2.rectangle(annotated_img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                
                # Setup label text
                label = f"{cls_name.capitalize()} {conf:.1%}"
                (lbl_w, lbl_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
                
                # Draw label background
                if int(y1) - lbl_h - 10 < 0:
                    cv2.rectangle(
                        annotated_img, 
                        (int(x1), int(y2)), 
                        (int(x1) + lbl_w + 10, int(y2) + lbl_h + 10), 
                        color, 
                        -1
                    )
                    cv2.putText(
                        annotated_img, 
                        label, 
                        (int(x1) + 5, int(y2) + lbl_h + 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.45, 
                        (255, 255, 255), 
                        1, 
                        cv2.LINE_AA
                    )
                else:
                    cv2.rectangle(
                        annotated_img, 
                        (int(x1), int(y1) - lbl_h - 10), 
                        (int(x1) + lbl_w + 10, int(y1)), 
                        color, 
                        -1
                    )
                    cv2.putText(
                        annotated_img, 
                        label, 
                        (int(x1) + 5, int(y1) - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.45, 
                        (255, 255, 255), 
                        1, 
                        cv2.LINE_AA
                    )
                
        # Encode annotated image to Base64
        _, encoded_img = cv2.imencode(".jpg", annotated_img)
        img_base64 = base64.b64encode(encoded_img).decode("utf-8")
        
        # Summary statistics
        counts = {
            "car": 0,
            "motorcycle": 0,
            "bus": 0,
            "truck": 0
        }
        for d in detections:
            counts[d["class"]] = counts.get(d["class"], 0) + 1
            
        return {
            "success": True,
            "detections": detections,
            "counts": counts,
            "annotated_image": f"data:image/jpeg;base64,{img_base64}",
            "summary": {
                "total_detected": len(detections),
                "image_width": w,
                "image_height": h
            }
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
