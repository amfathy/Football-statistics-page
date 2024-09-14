from ultralytics import YOLO
import os
import json

def run_detection(weights_path, test_image_path, save_dir):
    # Ensure save directory exists and clear previous results
    os.makedirs(save_dir, exist_ok=True)
    labels_file_path = os.path.join(save_dir, 'labels.json')
    
    # Clear previous results if any
    if os.path.exists(labels_file_path):
        os.remove(labels_file_path)

    model = YOLO(weights_path)
    
    # Perform inference on the test image
    results = model.predict(source=test_image_path)

    # Get the first result (assuming there's only one image)
    result = results[0]

    # Extract and print the label information
    label_dict = {}
    for box in result.boxes:
        confidence = box.conf[0].item()
        if confidence > 0.5:  # Filter by confidence
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = result.names[box.cls[0].item()]
            if label not in label_dict:
                label_dict[label] = []
            label_dict[label].append({'confidence': confidence, 'bbox': [x1, y1, x2, y2]})

    # Get the maximum confidence for each label
    labels_info = []
    for label, boxes in label_dict.items():
        max_box = max(boxes, key=lambda x: x['confidence'])
        labels_info.append({'label': label, 'confidence': max_box['confidence'], 'bbox': max_box['bbox']})
        print(f'Label: {label}, Confidence: {max_box["confidence"]:.2f}, BBox: {max_box["bbox"]}')

    return labels_info

def clear_previous_results():
    # Clear previous detection results
    detection_json_path = r'D:\college\GP\phase2\labels.json'
    if os.path.exists(detection_json_path):
        os.remove(detection_json_path)

    # Clear previous OCR results
    ocr_json_path = r'D:\college\GP\phase2\OCR\extracted_data.json'
    ocr_txt_path = r'D:\college\GP\phase2\OCR\extracted_data.txt'
    if os.path.exists(ocr_json_path):
        os.remove(ocr_json_path)
    if os.path.exists(ocr_txt_path):
        os.remove(ocr_txt_path)

    # Clear previous classification results
    classification_json_path = r'D:\college\GP\phase2\Classify_events\processed_classification.json'
    if os.path.exists(classification_json_path):
        os.remove(classification_json_path)

def Detection_main():
    clear_previous_results()

    weights_path = r'D:\college\GP\phase2\best1.pt'
    test_image_path = r'D:\college\GP\phase2\video_dividing\frames'
    save_dir = r'D:\college\GP\phase2'

    print("Starting object detection...")
    labels_info = run_detection(weights_path, test_image_path, save_dir)
    
    # Save labels_info to the desired JSON file
    labels_output_path = r'D:\college\GP\phase2\Model\labels.json'
    with open(labels_output_path, 'w') as labels_file:
        json.dump(labels_info, labels_file, indent=4)

    print(f"Object detection completed. Labels saved in {labels_output_path}.")

if __name__ == "__main__":
    Detection_main()
