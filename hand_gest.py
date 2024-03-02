import cv2
import mediapipe 

medhand=mediapipe.solutions.hands
med_draw=mediapipe.solutions.drawing_utils

hand=medhand.Hands(max_num_hands=1)

video=cv2.VideoCapture(0)
while True:
    success,image=video.read()
    imgrgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    result=hand.process(imgrgb)
    tipids=[4,8,12,16,20]
    lmlist=[]
    cv2.rectangle(image,(60,350),(90,150),(0,0,255),cv2.FILLED)
    cv2.rectangle(image,(60,350),(90,150),(0,0,255),6)

    if result.multi_hand_landmarks:
        for land_marks in result.multi_hand_landmarks:
            for id,lm in enumerate(land_marks.landmark):
                cx=lm.x
                cy=lm.y
                lmlist.append([id,cx,cy])

                if len(lmlist)!=0 and len(lmlist)==21:
                    finger_list=[]

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

                    for i in range(1,5):
                        if lmlist[tipids[i]][2]<lmlist[tipids[i]-2][2]:
                    
                            finger_list.append(1)
                        else:
                            finger_list.append(0)

            if len(finger_list)!=0:
                finger_list=finger_list.count(1)
                print(finger_list)

            cv2.putText(image,str(finger_list),(40,430),cv2.FONT_HERSHEY_COMPLEX,4,(0,0,255),3)
            med_draw.draw_landmarks(image,land_marks,medhand.HAND_CONNECTIONS ,
                                    med_draw.DrawingSpec(color=(0,255,0),thickness=4,circle_radius=3),
                                    med_draw.DrawingSpec(color=(0,255,0),thickness=4))


        
    cv2.imshow('HAND',image)
    if cv2.waitKey(1) & 0XFF==ord('q') :
        break

video.release()
cv2.destroyAllWindows()