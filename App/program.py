import sys
import os

sys.path.append(r'D:\college\GP\phase2')
sys.path.append(r'D:\college\GP\phase2\Model')
sys.path.append(r'D:\college\GP\phase2\video_dividing')
sys.path.append(r'D:\college\GP\phase2\OCR')
sys.path.append(r'D:\college\GP\phase2\Classify_events')

from video_dividing.upload import Upload_main
from Model.Detection import Detection_main
from OCR.OCR import OCR_main
from Classify_events.Classification import Classification_main 
from Streamlit.Streamlit import StreamLit_main

def Program_main():
    
#step 1:   
    print("Starting video frame extraction...")
    Upload_main()
    print("Video frame extraction completed.")

#step 2:
    print("Starting object detection...")
    Detection_main()
    print("Object detection completed.")

#step 3:
    print("Starting OCR processing...")
    OCR_main()
    print("OCR processing completed.")

#step 4:
    print("Starting classification...")
    Classification_main()
    print("Classification completed.")

#step 5:  
    print("StreamLit step...")
    StreamLit_main()
    print("StreamLit done...")

#clear Cache 
    clear_after_running()




def clear_after_running():
    detection_json_path = r'D:\college\GP\phase2\labels.json'
    if os.path.exists(detection_json_path):
        os.remove(detection_json_path)

    ocr_json_path = r'D:\college\GP\phase2\OCR\extracted_data.json'
    ocr_txt_path = r'D:\college\GP\phase2\OCR\extracted_data.txt'
    if os.path.exists(ocr_json_path):
        os.remove(ocr_json_path)
    if os.path.exists(ocr_txt_path):
        os.remove(ocr_txt_path)

    classification_json_path = r'D:\college\GP\phase2\Classify_events\processed_classification.json'
    if os.path.exists(classification_json_path):
        os.remove(classification_json_path)    

if __name__ == "__main__":
     Program_main()