# import necessary packages
import cv2 as cv
import numpy as np
import dlib 
from math import hypot
# using the inbuilt webcam 
cap=cv.VideoCapture(0)
# using dlib pre trained model
detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# computes mid points of coordinates
def midpoint(p1,p2):
    return int((p1.x+p2.x)/2),int((p1.y+p2.y)/2)

# function that ouptuts gaze ratio
def ratio(eye_points,facial_landmarks):
    # am array of coordinate points of the landmarks
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),(facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),(facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                            (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                            (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                            (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)
    # take the height of your original screen (basically creates a black image)
    height,width,_=frame.shape
    mask=np.zeros((height,width),np.uint8)
    # creates a polygon in that region; the value 255 specifies white color
    cv.polylines(mask,[left_eye_region],True,255,2)
    cv.fillPoly(mask,[left_eye_region],255)
    # shows the left eye with the pupil (black and white)
    eye=cv.bitwise_and(gray,gray,mask=mask)
    # gets all the eye points extremeties
    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])
    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv.threshold(gray_eye, 70, 255, cv.THRESH_BINARY)
    # divide the threshold into two parts
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    # All the zeros are black, so non-zeros will be white. Counting which part of the eyes has more white region
    left_side_white = cv.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv.countNonZero(right_side_threshold)
    # left side white and right side white will give you values
    # gaze values in this case is normalised to avoid division by zero
    if left_side_white==0:
        gaze_ratio=2

    elif right_side_white==0:
         gaze_ratio=5

    else: 
        gaze_ratio = left_side_white / right_side_white
    return(gaze_ratio)

# funtion for blink detection
def blink(eye_points,facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    # computes length of a line 
    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    ratio = hor_line_lenght / ver_line_lenght
    return ratio
# Continuous interations to output conditions based on function return values
while True:
    _,frame=cap.read()
    gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces=detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        # calling function for both left eye and right eye landmarks
        gaze_ratio_left_eye = ratio([36, 37, 38, 39, 40, 41], landmarks)
        gaze_ratio_right_eye = ratio([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
        left_eye_ratio = blink([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = blink([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
        if gaze_ratio <= 1:
            print("RIGHT")  
        elif 1 < gaze_ratio < 3:
            print("FORWARD")
        else:
            print("LEFT")
        
        if blinking_ratio > 5.7:
            print("Backward")
           
    cv.imshow("Frame",frame)
    key=cv.waitKey(10000)
    if key==ord('q'):
        break
cap.release()
cv.destroyAllWindows()    
