import cv2
import numpy as np
#from matplotlib import pyplot as plt


def region_of_interest(img,vertices):
    mask=np.zeros_like(img)
    #channel_count=img.shape[2]
    #match_mask_color=(255,)*channel_count
    cv2.fillPoly(mask,vertices,255)
    masked_img=cv2.bitwise_and(img,mask)
    return masked_img

def nothing(x):
    pass


cap=cv2.VideoCapture(r"D:\Downloads\Novak Djokovic vs Nick Kyrgios _ Gentlemen's Singles Final Highlights _ Wimbledon 2022.mp4")





_,frame1=cap.read()
_,frame2=cap.read()










while cap.isOpened():
    
    
    
    



    
    hsv1=cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)
    hsv2=cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)

    l_b=np.array([29,86,180])
    u_b=np.array([81,255,255])

   




    


    
    mask1=cv2.inRange(hsv1,l_b,u_b)
    
    mask1=cv2.erode(mask1,(1,1),iterations=2)
    mask1=cv2.dilate(mask1,(1,1),iterations=2)

    mask2=cv2.inRange(hsv2,l_b,u_b)
    
    mask2=cv2.erode(mask2,(1,1),iterations=2)
    mask2=cv2.dilate(mask2,(1,1),iterations=2)



    res1=cv2.bitwise_and(frame1,frame1,mask=mask1)
    res2=cv2.bitwise_and(frame2,frame2,mask=mask2)

    






    
    diff=cv2.absdiff(res1,res2)
    gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    
    _,thresh=cv2.threshold(gray,20,255,cv2.THRESH_BINARY)
    dilate=cv2.dilate(thresh,None,iterations=2)

    '''h=dilate.shape[0]
    w=dilate.shape[1]'''
    

    roi_vertices1=[(300,215),(928,215),(50,583),(1160,583)]
    #roi_vertices2=[(335,329),(968,329),(164,582),(1113,582)]

    

    masked_image1=region_of_interest(dilate,np.array([roi_vertices1],np.int32))
    #masked_image2=region_of_interest(dilate,np.array([roi_vertices2],np.int32))
    #masked_image=cv2.add(masked_image1,masked_image2)



    
    
    contours,_=cv2.findContours(masked_image1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #img_copy=masked_image.copy()
    #img_copy=cv2.cvtColor(img_copy,cv2.COLOR_GRAY2BGR)

    
    for c in contours:
        approx=cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
        
        
        if len(approx)>2 and len(approx)<30:
            x,y,w,h=cv2.boundingRect(c)
            if cv2.contourArea(c)>10 and cv2.contourArea(c)<150:

                cv2.rectangle(frame1,(x-3,y-3),(x+w+3,y+h+3),(255,0,0),4)

    

    

    
    

    
    cv2.imshow('test',frame1)
   
    frame1=frame2
    _,frame2=cap.read()
    
    

    if cv2.waitKey(40) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
