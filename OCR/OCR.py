import cv2
import easyocr
import numpy as np
import json
import os

def preprocess_image(image, target_width=1000):
    scale_factor = target_width / image.shape[1]
    resized_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    denoised_image = cv2.fastNlMeansDenoising(inverted_image, None, 7, 7, 21)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(denoised_image, -1, kernel)
    return sharpened_image

def crop_image(image, coordinates):
    x1, y1, x2, y2 = coordinates
    return image[y1:y2, x1:x2]

def extract_text_from_image(image_path, coordinates_list):
    image = cv2.imread(image_path)
    extracted_text = []

    for coordinates in coordinates_list:
        cropped_image = crop_image(image, coordinates)
        preprocessed_image = preprocess_image(cropped_image)
        temp_image_path = "temp_image.png"
        cv2.imwrite(temp_image_path, preprocessed_image)
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(temp_image_path)
        text = "\n".join([result[1] for result in results])
        extracted_text.append(text)

    return "\n".join(extracted_text)

def OCR_main():
    # Paths
    labels_file_path = r'D:\college\GP\phase2\Model\labels.json'
    frame_dir = r'D:\college\GP\phase2\video_dividing\frames'
    output_file_json = r"D:\college\GP\phase2\OCR\extracted_data.json"

    # Clear previous results
    if os.path.exists(output_file_json):
        os.remove(output_file_json)


    # Load labels
    with open(labels_file_path, 'r') as file:
        label_coordinates = json.load(file)
    
    extracted_data = {}
    last_event_info = {}

    # Iterate through the list of label coordinates
    for entry in label_coordinates:
        frame_number = entry.get("frame_number", "unknown_frame")
        labels = entry.get("labels", [])

        frame_path = os.path.join(frame_dir, f'{frame_number}.jpg')
        
        time_text = None
        if any(label['label'] == 'Time' for label in labels):
            time_text = extract_text_from_image(frame_path, [label['bbox'] for label in labels if label['label'] == 'Time'])
        
        if any(label['label'] == 'NP' for label in labels) and any(label['label'] == 'Event' for label in labels):
            players = extract_text_from_image(frame_path, [label['bbox'] for label in labels if label['label'] == 'NP'])
            events = extract_text_from_image(frame_path, [label['bbox'] for label in labels if label['label'] == 'Event'])
            
            if players and events:
                # Create a unique event key based on player and event text
                event_key = (players, events)
                
                # Check for duplicates within the same minute
                minute_key = time_text.split(":")[0] if time_text else frame_number
                if minute_key not in last_event_info or last_event_info[minute_key] != event_key:
                    extracted_data[frame_number] = {
                        "time": time_text if time_text else frame_number,
                        "player": players,
                        "event": events
                    }
                    last_event_info[minute_key] = event_key

    # Save results to JSON
    with open(output_file_json, 'w', encoding='utf-8') as file:
        json.dump(extracted_data, file, indent=4)

if __name__ == "__main__":
    OCR_main()
