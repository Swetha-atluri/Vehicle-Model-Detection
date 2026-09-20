# OmniDetect AI - Vehicle Detection Hub 🚗🚌🏍️

OmniDetect AI is a modern, responsive Web application designed to perform real-time vehicle detection and categorization. Utilizing a FastAPI backend powered by the **YOLOv8** object detection model and a glassmorphism frontend dashboard, the application identifies and counts cars, trucks, buses, and motorcycles in uploaded images.

---

## 🌟 Features

- **Futuristic Web Dashboard**: Glassmorphism design with sleek slate backgrounds and neon highlights (rose, emerald, amber, blue).
- **Drag & Drop Upload**: Interactive image upload panel with immediate client-side preview.
- **YOLOv8 Nano Core**: Fast and accurate object detection filtered specifically for vehicle classes.
- **Visualized Output**: Bounding boxes and confidence percentages drawn on the result image using custom class colors.
- **Detections Log**: A tabbed interactive logs table displaying coordinates, class labels, and confidence progress bars.
- **Robust Image Parsing**: Uses Pillow (PIL) for decoding, supporting JPEGs, transparent PNGs, and modern WebP formats seamlessly.

---

## 🛠️ Technology Stack

- **Backend**: FastAPI, Uvicorn (ASGI server)
- **AI Core**: Ultralytics YOLOv8, PyTorch
- **Image Processing**: OpenCV (headless), Pillow (PIL), NumPy
- **Frontend**: HTML5, Vanilla CSS3, JavaScript, FontAwesome Icons

---

## 📂 Project Structure

```text
├── static/
│   ├── css/
│   │   └── style.css       # Custom dashboard styling
│   ├── js/
│   │   └── app.js          # Client-side API requests and UI state
│   └── index.html          # Web dashboard layout
├── .gitignore              # Ignores venv, caches, and weights
├── main.py                 # FastAPI backend entry point
├── README.md               # Documentation
├── requirements.txt        # Python dependency packages list
└── test_api.py             # Script to verify API endpoint locally
```

---



### 5. Access the Web Dashboard
Open your browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

Upload any vehicle image (JPEG, PNG, WebP) and click **Run Detection**.
