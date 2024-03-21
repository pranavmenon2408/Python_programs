
# Python code for Multiple Color Detection
def region_of_interest(img,vertices):
    mask=np.zeros_like(img)
    #channel_count=img.shape[2]
    #match_mask_color=(255,)*channel_count
    cv2.fillPoly(mask,vertices,255)
    masked_img=cv2.bitwise_and(img,mask)
    return masked_img
import numpy as np 
import cv2 
  
  
# Capturing video through webcam 
cap = cv2.VideoCapture(0) 
roi_vertices1=[(0,0),(360,0),(360,400),(0,400)]
# Start a while loop 
while(1): 
      
    # Reading the video from the 
    # webcam in image frames 
    _, frame = cap.read() 
    imageFrame =frame.copy()
    # Convert the imageFrame in  
    # BGR(RGB color space) to  
    # HSV(hue-saturation-value) 
    # color space 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 
  
    # Set range for red color and  
    # define mask 
    red_lower = np.array([136, 87, 111], np.uint8) 
    red_upper = np.array([180, 255, 255], np.uint8) 
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 
    # Set range for blue color and 
    # define mask 
    purple_lower = np.array([147, 31, 137],np.uint8)
    purple_upper = np.array([170, 132, 201],np.uint8)
    purple_mask = cv2.inRange(hsvFrame, purple_lower, purple_upper) 
      
    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernel = np.ones((5, 5), "uint8") 
      
    # For red color 
    red_mask = cv2.dilate(red_mask, kernel)
    #red_mask=region_of_interest(red_mask,np.array([roi_vertices1],np.int32))
    res_red = cv2.bitwise_and(imageFrame, imageFrame,  
                              mask = red_mask)
      
    
    # For blue color 
    purple_mask = cv2.dilate(purple_mask, kernel)
    #purple_mask=region_of_interest(purple_mask,np.array([roi_vertices1],np.int32))
    res_purple = cv2.bitwise_and(imageFrame, imageFrame, mask = purple_mask)
   
    # Creating contour to track red color 
    contours, hierarchy = cv2.findContours(red_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
      
    for pic, c in enumerate(contours):
        if cv2.contourArea(c)>500:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 50:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(imageFrame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(imageFrame, center, 5, (0, 0, 255), -1)
 
  
    
  
    # Creating contour to track blue color 
    contours, hierarchy = cv2.findContours(purple_mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic, c in enumerate(contours):
        if cv2.contourArea(c)>500:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
            # only proceed if the radius meets a minimum size
            if radius > 50:
                
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(imageFrame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(imageFrame, center, 5, (0, 0, 255), -1)
              
    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", frame)
    
    cv2.imshow("res+red",red_mask)
    cv2.imshow("res+purple",purple_mask)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break