import requests
import json
import base64

url = "http://127.0.0.1:8000/api/detect"
files = {"file": open("vehicle_test_sample.jpg", "rb")}

try:
    print("Sending request to FastAPI backend...")
    response = requests.post(url, files=files)
    if response.status_code == 200:
        data = response.json()
        print("Success!")
        print("Detections summary:")
        print(json.dumps(data["summary"], indent=2))
        print("Counts:")
        print(json.dumps(data["counts"], indent=2))
        print(f"Total detections list size: {len(data['detections'])}")
        
        # Save base64 image back to verify drawing
        img_data = data["annotated_image"].split(",")[1]
        with open("annotated_result.jpg", "wb") as fh:
            fh.write(base64.b64decode(img_data))
        print("Annotated result saved as 'annotated_result.jpg'.")
    else:
        print(f"Failed with status: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error during API call: {e}")
