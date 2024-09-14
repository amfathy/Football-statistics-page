import streamlit as st
import json

def StreamLit_main():
    # Load processed events from JSON file
    processed_events_path = r'D:\college\GP\phase2\Classify_events\processed_classification.json'
    
    with open(processed_events_path, 'r') as file:
        processed_events = json.load(file)
    
    # Styling for the event box
    event_box_style = """
    <style>
    .event-box {
        background-color: #f0f0f0;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        border: 1px solid #ccc;
    }
    .event-header {
        font-weight: bold;
    }
    .icon {
        margin-right: 5px;
    }
    </style>
    """
    
    st.markdown(event_box_style, unsafe_allow_html=True)
    
    # Sort events by time
    processed_events.sort(key=lambda x: x['time'])  # Sort by event time
    
    # Create and display sorted event strings
    for event in processed_events:
        event_time = event['time']
        event_player = event['player']
        event_type = event['event']
        
        icon = ''
        if 'Goal' in event_type:
            icon = '⚽'
        elif 'sub' in event_type.lower():
            icon = '🔄'
        elif 'Yellow card' in event_type:
            icon = '🟨'
        elif 'Red card' in event_type:
            icon = '🟥'
        
        # Create event string
        event_string = f"{icon} {event_time} - **{event_player}** ({event_type})"
        
        # Display event
        st.markdown(f"<div class='event-box'>{event_string}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    StreamLit_main()
