import cv2
import numpy as np
import configparser
import logging
import logging.config

# Read the properties file
config = configparser.ConfigParser()
config.read('config.properties')


logConf = config.get('LogFile', 'logConfiguration')

logging.config.fileConfig(logConf)
logger = logging.getLogger('colorsync')

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def extractFeatures(image):
    logger.info("stared to process image")
    # Convert image to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Check if there is exactly one face in the image
    if len(faces) != 1:
        error_message = f"Detected {len(faces)} faces. Please provide an image with exactly one face."
        logger.error(f"Error occured:{error_message}")
        return {"error": error_message}  # Return an error message instead of exiting

    logger.info("detected only one face")
    # Get the coordinates of the detected face
    (x, y, w, h) = faces[0]

    # Crop the image to the detected face region for better processing
    face_region = image[y:y+h, x:x+w]

    # Convert the face region to HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)

    # --- Skin Color Detection ---
    # Define the range for skin color in HSV space (more refined range)
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)  # Adjusted lower bound
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)  # Adjusted upper bound

    # Create a mask for skin color
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Apply morphological operations to remove noise and smooth the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Apply the mask to extract the skin region
    skin = cv2.bitwise_and(face_region, face_region, mask=skin_mask)

    # Calculate the average skin color
    skin_pixels = cv2.countNonZero(skin_mask)
    if skin_pixels > 0:
        skin_avg = cv2.mean(face_region, mask=skin_mask)[:3]

    logger.info("skin color extraction completed")
    # --- Hair Color Detection ---
    # Convert the face region to grayscale
    gray_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection to detect hair edges
    edges = cv2.Canny(gray_face, 50, 150)

    # Apply morphological operations to enhance hair detection
    hair_mask = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Apply the mask to extract the hair region
    hair = cv2.bitwise_and(face_region, face_region, mask=hair_mask)

    # Calculate the average hair color
    hair_pixels = cv2.countNonZero(hair_mask)
    hair_avg = None
    if hair_pixels > 0:
        hair_avg = cv2.mean(face_region, mask=hair_mask)[:3]

    logger.info("hair color extraction completed")
    
    # --- Eye Color Detection using Haar Cascade ---
    # Load the Haar Cascade for detecting eyes
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Detect eyes in the face region
    eyes = eye_cascade.detectMultiScale(gray_face, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Iterate through the detected eyes
    eye_avg = None
    for (ex, ey, ew, eh) in eyes:
        # Draw a rectangle around the eye (for visualization)
        cv2.rectangle(face_region, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        # Extract the eye region from the face region
        eye_region = face_region[ey:ey + eh, ex:ex + ew]
        eye_hsv = cv2.cvtColor(eye_region, cv2.COLOR_BGR2HSV)

        # --- Refine Eye Color Detection ---
        # Define color range for eye color detection (based on hue range)
        lower_eye_hue = np.array([100, 50, 50], dtype=np.uint8)  # Hue range for blue/green eyes
        upper_eye_hue = np.array([140, 255, 255], dtype=np.uint8)  # Adjust as needed for blue/green

        # Create a mask for eye colors
        eye_mask = cv2.inRange(eye_hsv, lower_eye_hue, upper_eye_hue)
        
        # Apply the mask to extract the eye region color
        eye_colored = cv2.bitwise_and(eye_region, eye_region, mask=eye_mask)

        # Calculate the average color of the eye region after mask
        eye_avg = cv2.mean(eye_colored, mask=eye_mask)[:3]
    logger.info("eye color extraction completed")
    
    colors = [skin_avg, hair_avg, eye_avg]
    list_of_colors = colorcodes(colors)
    return list_of_colors
    


# Function to convert BGR to HEX color
def colorcodes(values):
    logger.info("hexa color coding started")
    colors_list =[]
    for i in values:
        if i is not None:  # Skip None values
            bgr_color = i
            # Convert to RGB (OpenCV uses BGR by default)
            rgb_color = (bgr_color[2], bgr_color[1], bgr_color[0])

            # Convert RGB to HEX format
            hex_color = "#{:02x}{:02x}{:02x}".format(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))
            colors_list.append(hex_color)
    logger.info("hexa color coding completed!")
    return colors_list
            

