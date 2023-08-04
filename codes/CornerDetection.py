import cv2
import numpy as np

img=cv2.imread(r"D:\arunv\Pranav\opencv-4.x\samples\data\chessboard.png")

img=cv2.resize(img,(512,512))

cv2.imshow('image',img)
#cv2.resizeWindow('image',512,512)




gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray=np.float32(gray)
dst=cv2.cornerHarris(gray,2,3,0.04)

dst=cv2.dilate(dst,None)

img[dst>0.01*dst.max()]=[0,0,255]
cv2.imshow('dst',img)


if cv2.waitKey(0)==ord('q'):
    cv2.destroyAllWindows()
                       