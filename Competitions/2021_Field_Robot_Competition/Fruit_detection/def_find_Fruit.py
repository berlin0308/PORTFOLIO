
def find_Fruit(frame):

    frame = cv2.resize(frame, (640, 480))

    x = 200
    y = 250
    w = 150
    h = 100

    polygon = np.array([[x,y], [x,y+h], [x+w,y+h], [x+w,y]])
    cv2.polylines(frame,pts=[polygon],isClosed=True,color=(90,120,225),thickness=3)

    cv2.imshow("original",frame)

    """ cropping """
    crop = frame[y:y+h, x:x+w]
    #cv2.imshow("cropped",crop)
    tomato_area, TOMATO, frame_tomato = find_tomato(crop,TOMATO_threshold,Hmin_red1_phase1, Smin_red1_phase1, Vmin_red1_phase1, Hmax_red1_phase1, Smax_red1_phase1, Vmax_red1_phase1, Hmin_red2_phase1, Smin_red2_phase1, Vmin_red2_phase1, Hmax_red2_phase1, Smax_red2_phase1, Vmax_red2_phase1)
    print("Tomato:",TOMATO,tomato_area)
    #cv2.imshow("Tomato",frame_tomato)

    lemon_area, LEMON, frame_lemon = find_lemon(crop,LEMON_threshold,Hmin_green_phase1,Smin_green_phase1,Vmin_green_phase1,Hmax_green_phase1,Vmax_green_phase1,Vmax_green_phase1)
    print("Lemon:",LEMON,lemon_area)
    #cv2.imshow("Lemon",frame_lemon)

    avocado_area, AVOCADO, frame_avocado = find_avocado(crop,AVOCADO_threshold,Hmin_black_phase1,Smin_black_phase1,Vmin_black_phase1,Hmax_black_phase1,Vmax_black_phase1,Vmax_black_phase1)
    print("Avocado:",AVOCADO,avocado_area)
    #cv2.imshow("Avocado",frame_avocado)

    crop = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
    Display_Fruits_1 =  cv2.hconcat([crop,frame_tomato])
    Display_Fruits_2 =  cv2.hconcat([frame_lemon,frame_avocado])
    Display_Fruits = cv2.vconcat([Display_Fruits_1,Display_Fruits_2])
    cv2.imshow("crop / tomato \n lemon / avocado",Display_Fruits)
                
    countFruit = 0
    for fruit in [TOMATO,LEMON,AVOCADO] :
        if fruit == True:
            countFruit += 1

    if countFruit == 0:
        print("No fruit is found...")
        return "void"
    elif countFruit == 1:
        #print("Only 1 is found")
        if TOMATO == True:
            print("\nOnly TOMATO is found")
            return "TOMATO"
        if LEMON == True:
            print("\nOnly LEMON is found")
            return "LEMON"
        if AVOCADO == True:
            print("\nOnly AVOCADO is found")
            return "AVOCADO"
    elif countFruit == 2:
        print("\n2 are found")
        return "void"
    elif countFruit == 3:
        print("\n3 are found")
        return "void"
        
