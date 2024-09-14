import json
import os
from collections import defaultdict

def process_classifications(classifications):
    processed_classifications = defaultdict(list)

    for frame_number, classification in classifications.items():
        time = classification.get('time')
        player = classification.get('player')
        classification_type = classification.get('event')

        if time is None or player is None or classification_type is None:
            continue
        
        # Normalize time format
        time = time.replace('.', ':').replace('*', ':')

        key = (player.strip(), classification_type)  # Use strip to remove extra spaces

        # Convert time to seconds for comparison
        minutes, seconds = map(float, time.split(":"))
        total_seconds = int(minutes * 60 + seconds)

        # Add classification to the list
        processed_classifications[key].append((frame_number, total_seconds))

    unique_classifications = []

    for key, times in processed_classifications.items():
        times.sort(key=lambda x: x[1])  # Sort by time

        for idx, (frame_number, t) in enumerate(times):
            minutes = t // 60
            seconds = t % 60
            
            # Handle substitutions
            if key[1] == "Substitution":
                player_names = key[0].split('\n')
                combined_player = "\n".join(sorted(player_names))  # Sort to ensure uniqueness

                # Check for duplicates within the same minute and frame difference
                if unique_classifications:
                    last_classification = unique_classifications[-1]
                    last_frame = last_classification['frame']
                    last_time = last_classification['time']
                    last_event_type = last_classification['event']
                    last_minutes, last_seconds = map(int, last_time.split(':'))
                    last_total_seconds = last_minutes * 60 + last_seconds
                    
                    # Check if within the same minute and frame difference < 3
                    if (minutes == last_minutes and 
                        abs(int(frame_number.split('_')[1]) - int(last_frame.split('_')[1])) < 3):
                        continue  # Skip duplicate classifications

                # Add substitution classification
                unique_classifications.append({
                    'frame': frame_number,
                    'time': f"{int(minutes)}:{int(seconds):02}",
                    'player': combined_player,
                    'event': key[1]
                })
                continue

            # For other classifications, check for duplicates within the same minute
            if unique_classifications and unique_classifications[-1]['event'] == key[1]:
                last_time = unique_classifications[-1]['time']
                last_minutes, last_seconds = map(int, last_time.split(':'))
                last_total_seconds = last_minutes * 60 + last_seconds
                
                if abs(total_seconds - last_total_seconds) < 4:
                    continue  # Skip duplicates

            unique_classifications.append({
                'frame': frame_number,
                'time': f"{int(minutes)}:{int(seconds):02}",
                'player': key[0],
                'event': key[1]
            })

    return sorted(unique_classifications, key=lambda x: x['time'])

def Classification_main(): 
    
    output_file_path = r'D:\college\GP\phase2\Classify_events\processed_classification.json'
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    file_path = r'D:\college\GP\phase2\OCR\extracted_data.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    processed_classifications = process_classifications(data)
    
    with open(output_file_path, 'w') as file:
        json.dump(processed_classifications, file, indent=4)
        

if __name__ == "__main__":
    Classification_main()
