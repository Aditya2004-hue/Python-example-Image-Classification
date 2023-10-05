import requests
import json
import cv2
import numpy as np
import os

# Load the image
image_path = "path of input image"
output_dir = "path to store image"
image = cv2.imread(image_path)

# Convert the image to base64 string
_, image_data = cv2.imencode('.jpg', image) 
image_base64 = image_data.tobytes()

# Sending request to BrainyPi
url = "url of server"  
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data = image_data.tobytes())
#Save the result
def save_image(image, image_path,output_dir):
   
    print("Saving output image to dir {}".format(output_dir))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = "result_{}".format(image_path.split('/')[-1])
    filepath = os.path.join(output_dir, filename)
    cv2.imwrite(filepath, image)

#displaying image
def display_image(image):
    cv2.imshow("Image", image)
    cv2.waitKey(0)


if response.status_code == 200: 
    response_data = response.json() 
    print(response.json())
    classes = response_data["result"]["classes"]
    print(classes)

    
    # Extracting text for drawing 
    text = ""
    for i, class_info in enumerate(classes):
        class_name = class_info["class"]
        confidence = class_info["confidence"]
        text += f"{class_name}: {confidence:.2f}"
        if i != len(classes) - 1:
            text += "\n"
    # Draw the text on the image using OpenCV
    text_position = (10, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_color = (0, 0, 255)
    line_type = 2
    cv2.putText(image, text, text_position, font, font_scale, font_color, line_type)

    save_image(image, image_path,output_dir)
    
    display_image(image)
else:
    print("Error: Request to the API server failed ", response.status_code)
