import cv2
import mediapipe 

mphands=mediapipe.solutions.hands
draw=mediapipe.solutions.drawing_utils

Hand=mphands.Hands(max_num_hands=1)

video=cv2.VideoCapture(0)
while True:
    success,image=video.read()
    imgrgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    result=Hand.process(imgrgb)
    tipids=[4,8,12,16,20]
    lmlist=[]
    #cv2.rectangle(image,(30,350),(90,420),(0,255,0),cv2.FILLED)
    cv2.rectangle(image,(30,350),(90,420),(0,255,0),4)
    if result.multi_hand_landmarks:
        for land_marks in result.multi_hand_landmarks: 
            for id,lm in enumerate(land_marks.landmark):
               # print(id,lm)
                  cx=lm.x
                  cy=lm.y
                  lmlist.append([id,cx,cy])
                  #print(lmlist)

                  if len(lmlist)!=0 and len(lmlist)==21:
                      finger_list=[]


                      # thumb

                      if lmlist[20][1]<lmlist[12][1]:
                          if lmlist[4][1]<lmlist[3][1]:
                              finger_list.append(0)
                          else:
                              finger_list.append(1)
                      else:
                          if lmlist[4][1]>lmlist[3][1]:
                              finger_list.append(0)
                          else:
                              finger_list.append(1)
                        


                    # other fingers
                      for i in range(1,5):
                          if lmlist[tipids[i]][2]<lmlist[tipids[i]-2][2]:
                              finger_list.append(1)
                          else:
                              finger_list.append(0)
                      #print(finger_list)
                              
            if len(finger_list)!=0:
                fingercount=finger_list.count(1)
                print(fingercount)                                                                     


            text=cv2.putText(image,str(fingercount),(40,450),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),5)
            draw.draw_landmarks(image,land_marks,mphands.HAND_CONNECTIONS,
                                draw.DrawingSpec(color=(255,255,255),thickness=4,circle_radius=3),
                                draw.DrawingSpec(color=(0,0,255),thickness=4))  
    cv2.imshow("Hand",image)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
video.release()
cv2.destroyAllWindows()

