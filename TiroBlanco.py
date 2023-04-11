import cv2
import numpy as np
import time


cap = cv2.VideoCapture(0)

cx_P = 0
cx_L =0
cy_P =0 
cy_L=0
Distacia=0
puntaje = 0
jugador = 1
while True:
    ret, frame = cap.read()
    '''width = int(cap.get(3))
    height = int(cap.get(4))'''


    # Aplicando Filtro Gaussiano
    frame = cv2.GaussianBlur(frame, (5, 5), cv2.BORDER_DEFAULT)
    cv2.imshow("image_blur", frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_array_L = np.array([159, 44, 0])
    upper_array_L = np.array([169, 213, 240])

    lower_array_P = np.array([59, 54, 0])
    upper_array_P = np.array([101, 205, 232])
    mask_L = cv2.inRange(hsv, lower_array_L, upper_array_L)
    mask_P = cv2.inRange(hsv, lower_array_P, upper_array_P)


    '''result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("Result", result)'''

    # Buscamos los contornos exteriores
    counts_L = cv2.findContours(mask_L, cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)[-2]
    counts_P = cv2.findContours(mask_P, cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)[-2]

    try:
        for i in range(len(counts_P)):
            cnt = counts_P[i]
            M = cv2.moments(cnt)
            cx_P = int(M["m10"]/M["m00"])
            cy_P = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx_P,cy_P),5,(0,255,0),-1)
            # imagen, texto, posicion, tipo, escala, colordetexto, grosor
            cv2.putText(frame,"x: "+str(cx_P)+", y: "+str(cy_P),(cx_P,cy_P),1,1,(0,0,0),1)
    except:
        print('error2')
        print(counts_P)

    try:
        for i in range(len(counts_L)):
            cnt = counts_L[i]
            M = cv2.moments(cnt)
            cx_L = int(M["m10"]/M["m00"])
            cy_L = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx_L,cy_L),5,(0,255,0),-1)

            cx= pow((cx_P - cx_L),2)
            cy= pow((cy_P - cy_L),2)
            Distacia = np.sqrt(cx+cy)
            print("Distacia")
            print(Distacia)
            # imagen, texto, posicion, tipo, escala, colordetexto, grosor
            cv2.putText(frame,"x: "+str(cx_L)+", y: "+str(cy_L),(cx_L,cy_L),1,1,(0,0,0),1)
            
            time.sleep(1)
    except:
        print('error1')


    
    
    # Rellenamos los contornos
    # cv2.drawContours(mask, counts, -1, 255, -1)
    cv2.drawContours(frame, counts_L, -1, (0, 255, 0), 2)
    cv2.drawContours(frame, counts_P, -1, (0, 255, 0), 2)
   
    if Distacia>160:
        puntaje =puntaje+0
    if Distacia>133 and Distacia <160:
        puntaje =puntaje+1
    if Distacia>104 and Distacia <130:
        puntaje =puntaje+2
    if Distacia>80 and Distacia <100:
        puntaje =puntaje+3
    if Distacia>60 and Distacia <78:
        puntaje =puntaje+4
    if Distacia>44 and Distacia <58:
        puntaje =puntaje+5
    if Distacia <40 and Distacia >10:
        puntaje =puntaje+10
    
    cv2.putText(frame,"D: "+str(Distacia),(10,120),1,2,(0,0,0),2)
    #cv2.putText(frame,"Jugador N: "+str(jugador),(10,150),1,2,(0,0,0),2)
    cv2.putText(frame,"Puntaje: "+str(puntaje),(10,180),1,2,(0,0,0),2)

    cv2.imshow('frame', frame)
    '''cv2.imshow("Mask L", mask_L)
    cv2.imshow("Mask P", mask_P)'''

    counts_P = 0
    counts_L = 0
    Distacia=0
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()