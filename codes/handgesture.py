import cv2
import mediapipe as mp

class HandGesture(object):
    def __init__(self):
        pass
    def map(self,v,in_min,in_max,out_min,out_max):
       if v<in_min:
           v= in_min 
       if v>in_max:
           v=in_max
       return (v-in_min)*(out_max-out_min)//(in_max-in_min)+out_min
    def hand(self):
       mp_drawing = mp.solutions.drawing_utils
       mp_drawing_styles = mp.solutions.drawing_styles
       mp_hands = mp.solutions.hands
       cap = cv2.VideoCapture(0)
#flag=False
       with mp_hands.Hands(
         model_complexity=0,
         min_detection_confidence=0.5,
         min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
         _,frame=cap.read()
         h=frame.shape[0]
         w=frame.shape[1]
         

         frame.flags.writeable=False
         frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
         results=hands.process(frame)
        
         frame.flags.writeable=True
         frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
         flag=False
         thumb=0
         if results.multi_hand_landmarks:

            #print(results.multi_hand_landmarks)
            for hand_landmarks in results.multi_hand_landmarks:
                handLandmarks=[]
                for landmarks in hand_landmarks.landmark:
                    handLandmarks.append([landmarks.x,landmarks.y])
                

                x1=int(self.map(handLandmarks[4][0],0,1,0,w))
                x2=int(self.map(handLandmarks[20][0],0,1,0,w))
                
                y1=int(self.map(handLandmarks[4][1],0,1,0,h))
                y3=int(self.map(handLandmarks[3][1],0,1,0,h))
                y2=int(self.map(handLandmarks[20][1],0,1,0,h))

                #speed=self.map(self.euclidean_distance(handLandmarks[4],handLandmarks[8]),0,0.6,0,255)
                #str_speed="SPEED : "+str(speed)



                mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
                flag=True
                if(y3-y1>20 and y2-y1>30 and abs(x2-x1)<25):
                   thumb=1

                #print(hand_landmarks)
         if flag and thumb:        
            #cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),5)
            cv2.putText(frame,"THUMBS UP",(200,320),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
         cv2.imshow("HAND TRACK",frame)
         if cv2.waitKey(1)==ord('q'):
            break
       cap.release()
       cv2.destroyAllWindows()

if __name__=="__main__":
   try:
      x=HandGesture()
      x.hand()
   except KeyboardInterrupt:
      print("Exit")

