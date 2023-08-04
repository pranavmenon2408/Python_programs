import cv2

face_cascade=cv2.CascadeClassifier(r"D:\arunv\Pranav\opencv-4.x\data\haarcascades\haarcascade_frontalface_default.xml")
eye_cascade=cv2.CascadeClassifier(r"D:\arunv\Pranav\opencv-4.x\data\haarcascades\haarcascade_eye_tree_eyeglasses.xml")
#img=cv2.imread(r"D:\arunv\Pranav\PranavMenon.png")
#gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cap=cv2.VideoCapture(0)
while(cap.isOpened()):
    _,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    face= face_cascade.detectMultiScale(gray,1.1,4)

    for (x,y,w,h) in face:
          cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
          roi_gray=gray[y:y+h,x:x+w]
          roi_color=img[y:y+h,x:x+w]
          
          eye=eye_cascade.detectMultiScale(roi_gray,1.1,4)
          for(ex,ey,ew,eh) in eye:
               cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),5)

    cv2.imshow('Image',img)
    if cv2.waitKey(1)==ord('q'):
         break
cap.release()
cv2.destroyAllWindows()