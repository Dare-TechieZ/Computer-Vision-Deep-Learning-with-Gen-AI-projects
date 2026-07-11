import cv2
import numpy as np
import os

if not os.path.exists("Captured"):# to store all the captured imgs
    os.makedirs("Captured")

# FILTER FUNCTIONS

def normal(img):
    return img

def black_white(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def sepia(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])

    sepia_img = cv2.transform(img, kernel)
    sepia_img = np.clip(sepia_img, 0, 255)
    return sepia_img.astype(np.uint8)

def sketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blur = cv2.GaussianBlur(inverted, (21,21), 0)
    inverted_blur = 255 - blur
    sketch_img = cv2.divide(gray, inverted_blur, scale=256)
    return sketch_img

def cool_filter(img):
    b, g, r = cv2.split(img)
    b = cv2.add(b, 40)
    r = cv2.subtract(r, 20)
    cool = cv2.merge((b, g, r))
    return cool

def vintage(img):
    blue = img[:,:,0]
    green = img[:,:,1]
    red = img[:,:,2]

    red = cv2.add(red,30)
    green = cv2.add(green,15)
    blue = cv2.subtract(blue,15)
    vintage = cv2.merge((blue,green,red))
    return vintage

def warm_filter(img):
    b,g,r = cv2.split(img)
    r = cv2.add(r,40)
    b = cv2.subtract(b,20)
    warm = cv2.merge((b,g,r))
    return warm


cap = cv2.VideoCapture(0) # to capture from system webcam
current_filter = "Normal"

print("\nControls")
print("-----------------------")
print("1 -> Normal")
print("2 -> Black & White")
print("3 -> Sepia")
print("4 -> Sketch")
print("5 -> Cool")
print("6 -> Vintage")
print("7 -> Warm Filter (Custom)")
print("c -> Capture Image")
print("q -> Quit\n")

image_count = 1

while True:
    ret, frame = cap.read()
    if not ret:
        break
    output = frame.copy()

    if current_filter == "Normal":
        output = normal(frame)

    elif current_filter == "BW":
        output = black_white(frame)

    elif current_filter == "Sepia":
        output = sepia(frame)

    elif current_filter == "Sketch":
        output = sketch(frame)

    elif current_filter == "Cool":
        output = cool_filter(frame)

    elif current_filter == "Vintage":
        output = vintage(frame)

    elif current_filter == "Warm":
        output = warm_filter(frame)

    display = output.copy()

    if len(display.shape) == 2:
        display = cv2.cvtColor(display, cv2.COLOR_GRAY2BGR)

    cv2.putText(display,
                f"Filter : {current_filter}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)

    cv2.imshow("Instagram/Snapchat Filters", display)
    key = cv2.waitKey(1) & 0xFF

    #setting keys
    if key == ord('1'):
        current_filter = "Normal"

    elif key == ord('2'):
        current_filter = "BW"

    elif key == ord('3'):
        current_filter = "Sepia"

    elif key == ord('4'):
        current_filter = "Sketch"

    elif key == ord('5'):
        current_filter = "Cool"

    elif key == ord('6'):
        current_filter = "Vintage"

    elif key == ord('7'):
        current_filter = "Warm"

    elif key == ord('c'):

        filename = f"Captured/image_{image_count}.png"

        # saving whatevr is displayed to user
        cv2.imwrite(filename, output)

        print(f"Saved: {filename}")

        image_count += 1
    elif key == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
