import cv2
import numpy as np
from sklearn.metrics import pairwise


# GLOBAL VARIABLES
background = None
accumulated_weight = .5
roi_top = 20
roi_bottom = 300
roi_right = 300
roi_left = 600


def calc_accum_avg(frame, accumulated_weight):
  '''
  Given a frame and a previous accumulated weight, computed the weighted average of the image passed in.
  '''
  
  # GRAB THE BACKGROUND
  global background
  
  # FOR FIRST TIME, CREATE THE BACKGROUND FROM A COPY OF THE FRAME.
  if background is None:
    background = frame.copy().astype("float")
    return None
  
  # COMPUTE WEIGHTED AVERAGE, ACCUMULATE IT AND UPDATE THE BACKGROUND
  cv2.accumulateWeighted(frame, background, accumulated_weight)



def segment(frame, threshold=25):
  global background

  # CALCULATES THE ABSOLUTE DIFFERENTCE BETWEEN THE BACKGROUD AND THE PASSED IN FRAME
  diff = cv2.absdiff(background.astype("uint8"), frame)

  # APPLY A THRESHOLD TO THE IMAGE SO WE CAN GRAB THE FOREGROUND
  # WE ONLY NEED THE THRESHOLD, SO WE WILL THROW AWAY THE FIRST ITEM IN THE TUPLE WITH AN UNDERSCORE _
  _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

  # GRAB THE EXTERNAL CONTOURS FORM THE IMAGE
  # AGAIN, ONLY GRABBING WHAT WE NEED HERE AND THROWING AWAY THE REST
  contours, hierarchy = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  if len(contours) == 0:

    return None
  
  else:
  
    # GIVEN THE WAY WE ARE USING THE PROGRAM, THE LARGEST EXTERNAL CONTOUR SHOULD BE THE HAND (LARGEST BY AREA)
    # THIS WILL BE OUR SEGMENT
    hand_segment = max(contours, key=cv2.contourArea)
  
    return (thresholded, hand_segment)



def count_fingers(thresholded, hand_segment):
  
    # CALCULATED THE CONVEX HULL OF THE HAND SEGMENT
    conv_hull = cv2.convexHull(hand_segment)
  
   
    # FIND THE TOP, BOTTOM, LEFT , AND RIGHT.
    # THEN MAKE SURE THEY ARE IN TUPLE FORMAT
    top = tuple(conv_hull[conv_hull[:, :, 1].argmin()][0])
    bottom = tuple(conv_hull[conv_hull[:, :, 1].argmax()][0])
    left = tuple(conv_hull[conv_hull[:, :, 0].argmin()][0])
    right = tuple(conv_hull[conv_hull[:, :, 0].argmax()][0])
  
    # IN THEORY, THE CENTER OF THE HAND IS HALF WAY BETWEEN THE TOP AND BOTTOM AND HALFWAY BETWEEN LEFT AND RIGHT
    cX = (left[0] + right[0]) // 2
    cY = (top[1] + bottom[1]) // 2
  
    # FIND THE MAXIMUM EUCLIDEAN DISTANCE BETWEEN THE CENTER OF THE PALM
    # AND THE MOST EXTREME POINTS OF THE CONVEX HULL
  
    # CALCULATE DE EUCLIDEAN DISTANCE BETWEEN CENTER AND EXTREME POINTS
    distance = pairwise.euclidean_distances([(cX, cY)], Y=[left, right, top, bottom])[0]
  
    # Grab the largest distance
    max_distance = distance.max()
  
    # CREATE A CIRCLE WITH 80% RADIUS OF THE MAX EUCLIDEAN DISTANCE
    radius = int(0.8 * max_distance)
    circumference = (2 * np.pi * radius)
  
    # NOT GRAB AN ROI OF ONLY THAT CIRCLE
    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
  
    cv2.circle(circular_roi, (cX, cY), radius, 255, 10)
  
    # USING BIT-WISE AND WITH THE CIRLE ROI AS A MASK.
    # THIS THEN RETURNS THE CUT OUT OBTAINED USING THE MASK ON THE THRESHOLDED HAND IMAGE.
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)
  
    # USE THE CIRCLE TO PUT CONTOURS AROUND EVERYTHING THAT'S OUT A CERTAIN REGION
    contours, hierarchy = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  
    count = 0
  
    for cnt in contours:
    
      (x, y, w, h) = cv2.boundingRect(cnt)
    
      # INCREMENT COUNT OF FINGERS BASED ON TWO CONDITIONS:
    
      # 1. CONTOUR REGION IS NOT THE VERY BOTTOM OF HAND AREA (THE WRIST)
      out_of_wrist = ((cY + (cY * 0.25)) > (y + h))
    
      # 2. NUMBER OF POINTS ALONG THE CONTOUR DOES NOT EXCEED 25% OF THE CIRCUMFERENCE 
      # OF THE CIRCULAR ROI (OTHERWISE WE'RE COUNTING POINTS OFF THE HAND)
      limit_points = ((circumference * 0.25) > cnt.shape[0])
    
      if out_of_wrist and limit_points:
        count += 1
  
    return count


cam = cv2.VideoCapture(0)

num_frames = 0


while True:

  ret, frame = cam.read()
  
  # FLIP THE FRAME SO THAT IT IS NOT THE MIRROR VIEW
  frame = cv2.flip(frame, 1)
  
  frame_copy = frame.copy()
  
  # GRAB THE ROI FROM THE FRAME
  roi = frame[roi_top:roi_bottom, roi_right:roi_left]
  
  gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (7, 7), 0)
  
  # FOR THE FIRST 30 FRAMES WE WILL CALCULATE THE AVERAGE OF THE BACKGROUND.
  # WE WILL TELL THE USER WHILE THIS IS HAPPENING
  if num_frames < 60:
    calc_accum_avg(gray, accumulated_weight)
    if num_frames <= 59:
      cv2.putText(frame_copy, "WAIT! GETTING BACKGROUND AVG.", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      cv2.imshow("Finger Count", frame_copy)
  
  else:
    

    hand = segment(gray)
    

    if hand is not None:

      thresholded, hand_segment = hand
      
      # DRAW CONTOURS AROUND HAND SEGMENT
      cv2.drawContours(frame_copy, [hand_segment + (roi_right, roi_top)], -1, (255, 0, 0), 1)
      
      # COUNT THE FINGERS
      fingers = count_fingers(thresholded, hand_segment)
      
      cv2.putText(frame_copy, str(fingers), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      
      cv2.imshow("Thesholded", thresholded)
  
  # DRAW ROI RECTANGLE ON FRAME COPY
  cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0, 0, 255), 5)
  
  
  num_frames += 1
  
  # DISPLAY THE FRAME WITH SEGMENTED HAND
  cv2.imshow("Finger Count", frame_copy)
  
  k = cv2.waitKey(1) & 0xFF
  
  if k == 27:
    break

cam.release()
cv2.destroyAllWindows()