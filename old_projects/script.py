import cv2
import numpy as np

# Load pre-trained Haar Cascade for card detection (update this path to your own XML file)
# Example: Using a placeholder Haar Cascade for demonstration
card_cascade_path = 'path_to_your_card_cascade.xml'  # Replace with your path
card_cascade = cv2.CascadeClassifier(card_cascade_path)

# Function to detect cards in the frame
def detect_cards(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cards = card_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
    detected_cards = []

    for (x, y, w, h) in cards:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Draw rectangle around detected cards
        detected_cards.append((x, y, w, h))  # Log the position of detected cards

    return detected_cards

# Function to log player actions (Placeholder for action recognition)
def log_action(action):
    print(f"Player Action: {action}")  # This is where you log or save the action

# Function to process each frame
def process_frame(frame):
    detected_cards = detect_cards(frame)  # Detect cards in the current frame
    if detected_cards:
        print(f"Detected Cards: {len(detected_cards)}")  # Log detected card count

    cv2.imshow('Poker Game', frame)  # Display the frame

def main(video_path):
    # Load video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.")
            break
        
        # Process the current frame
        process_frame(frame)

        # Example of logging a player action (replace with real detection logic)
        log_action("Bet")  # Placeholder; you can implement detection logic here

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "C:/Users/Junjie/Video.MOV"  # Update with your video path
    # Ensure you have the correct path for the Haar Cascade
    if not cv2.CascadeClassifier(card_cascade_path).empty():
        main(video_path)
    else:
        print("Error: Could not load Haar Cascade XML file.")
