# OmniDetect AI — Vehicle Detection Hub

A real-time vehicle detection and classification web application powered by **YOLOv8** and **FastAPI**. The system analyzes uploaded images, detects vehicles, identifies their classes, and provides confidence scores along with visualized detection results.

---

## Overview

**OmniDetect AI** is a computer vision application designed to detect and categorize vehicles from images.

The application uses the **YOLOv8 object detection model** to identify vehicle classes such as cars, trucks, buses, and motorcycles. A **FastAPI** backend handles image processing and inference, while a responsive web dashboard provides an interactive interface for uploading images and viewing detection results.

The system visualizes detected objects using bounding boxes and confidence scores, while also providing a structured detection log containing class labels and coordinates.

---

## Key Features

- **Real-Time Vehicle Detection**  
  Detects multiple vehicles within uploaded images using YOLOv8.

- **Vehicle Classification**  
  Identifies supported vehicle categories including cars, trucks, buses, and motorcycles.

- **Interactive Web Dashboard**  
  Provides a responsive interface for uploading images and viewing detection results.

- **Drag-and-Drop Upload**  
  Supports convenient image selection with client-side preview.

- **Bounding Box Visualization**  
  Displays detected vehicles with bounding boxes, class labels, and confidence scores.

- **Detection Log**  
  Presents structured detection information including object classes, coordinates, and confidence values.

- **Multiple Image Formats**  
  Supports JPEG, PNG, and WebP image formats through Pillow.

- **Fast API-Based Inference**  
  Uses FastAPI and Uvicorn to provide an efficient backend for model inference.

---

## System Architecture

```text
                    User
                     |
                     v
          +----------------------+
          |   Web Dashboard      |
          | HTML / CSS / JS      |
          +----------+-----------+
                     |
                     | Image Upload
                     v
          +----------------------+
          |    FastAPI Backend   |
          +----------+-----------+
                     |
                     v
          +----------------------+
          |    Image Processing  |
          | OpenCV / Pillow      |
          +----------+-----------+
                     |
                     v
          +----------------------+
          |      YOLOv8 Model    |
          |  Vehicle Detection   |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Detection Results    |
          | Class + Confidence   |
          | Bounding Coordinates |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Visualized Dashboard |
          +----------------------+
