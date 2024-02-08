import cv2

# Function to select ROI
def select_roi(event, x, y, flags, param):
    global bbox, frame, frame_copy, tracking
    if event == cv2.EVENT_LBUTTONDOWN:
        bbox = (x, y, 1, 1)
        tracking = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if tracking:
            bbox = (bbox[0], bbox[1], x - bbox[0], y - bbox[1])
            frame_copy = frame.copy()
            cv2.rectangle(frame_copy, (bbox[0], bbox[1]), (x, y), (0, 255, 0), 2)
            cv2.imshow('Select ROI', frame_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        tracking = False

# Open the video file
video_path = '/home/instructor/Documents/OpenCV/CVFInalProj/CVProject/CVProject/IMG_8866.mov'
cap = cv2.VideoCapture(video_path)

# Check if video file opened successfully
if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

# Read the first frame
ret, frame = cap.read()
if not ret:
    print("Error: Unable to read the first frame.")
    exit()

# Select ROI (Region of Interest) for tracking
bbox = cv2.selectROI('Select ROI', frame, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

# Initialize CSRT tracker
tracker = cv2.TrackerCSRT_create()
ok = tracker.init(frame, bbox)

# Loop through the video frames
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Check if tracking was successful
    if ok:
        # Get the ROI within the bounding box
        roi = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]

        # Convert ROI to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Apply thresholding or other preprocessing if needed
        _, thresh = cv2.threshold(gray_roi, 127, 255, cv2.THRESH_BINARY)

        # Find contours in the ROI
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on the ROI
        cv2.drawContours(roi, contours, -1, (0, 0, 255), 2)

        # Display the frame with ROI
        cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
