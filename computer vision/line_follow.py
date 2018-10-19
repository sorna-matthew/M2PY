from pyueye import ueye
import numpy as np
import cv2
import m2py as mp
import matplotlib.pyplot as plt
 
def follow():
    
    #Open printer communication and set properties
    m = mp.Makergear('COM3',115200)
    m.coord(coord_sys = 'rel')
    m.move(z = -.1)
    m.move(z = .1)
    m.speed(speed = 30)
    
    
    # Initialize camera
    hcam = ueye.HIDS(0)
    ret = ueye.is_InitCamera(hcam, None)
    #print(f"initCamera returns {ret}")
 
    # set color mode
    ret = ueye.is_SetColorMode(hcam, ueye.IS_CM_BGR8_PACKED)
    #print(f"SetColorMode IS_CM_BGR8_PACKED returns {ret}")
    
    ueye.is_SetHWGainFactor(hcam, ueye.IS_SET_MASTER_GAIN_FACTOR, ueye.c_int(357))
    ret = ueye.is_SetHWGainFactor(hcam, ueye.IS_GET_MASTER_GAIN_FACTOR, ueye.c_int(100))
 
    # set region of interest
    width = 800
    height = 600
    rect_aoi = ueye.IS_RECT()
    rect_aoi.s32X = ueye.int(0)
    rect_aoi.s32Y = ueye.int(0)
    rect_aoi.s32Width = ueye.int(width)
    rect_aoi.s32Height = ueye.int(height)
    ueye.is_AOI(hcam, ueye.IS_AOI_IMAGE_SET_AOI, rect_aoi, ueye.sizeof(rect_aoi))
 
    # allocate memory
    mem_ptr = ueye.c_mem_p()
    mem_id = ueye.int()
    bitspixel = 24 # for colormode = IS_CM_BGR8_PACKED
    ret = ueye.is_AllocImageMem(hcam, width, height, bitspixel, mem_ptr, mem_id)
    ret = ueye.is_SetImageMem(hcam, mem_ptr, mem_id)
    ret = ueye.is_CaptureVideo(hcam, ueye.IS_DONT_WAIT)
    lineinc = width * int((bitspixel + 7) / 8)
    
    # Line tracking initializtion
    ct = 0
    cx0 = width/2
    cy0 = height/2
    direction = 1
    dx0 = 0
    dy0 = 0
    dir_x = [0]
    dir_y = [0]
    xtr = [0]
    ytr = [0]
    gamma = 0
    
    while True:
        img = ueye.get_data(mem_ptr, width, height, bitspixel, lineinc, copy=True)
        img = np.reshape(img, (height, width, 3))
        
        # Image Processing
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imblur = cv2.medianBlur(imgray, 15)
        ret, thresh = cv2.threshold(imblur, 60, 255, 1)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
        
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            img = cv2.circle(img,(cx, cy), 10, (0,255,0), -1) # Centroid marker
            (x,y),(MA,ma),angle = cv2.fitEllipse(c)
            alpha = angle - 90
            beta = 90 - angle
            
        # Keep on the line
        S = 0.2
        tracking_radius = 50
        D = np.sqrt((cx - cx0)**2 + (cy - cy0)**2)
        dx1 = (cx - cx0)/D
        dy1 = (cy - cy0)/D
        img = cv2.arrowedLine(img, (int(cx0), int(cy0)), (int(cx), int(cy)), (0,0,255), 5)
    
        if D > tracking_radius:    
            m.move(x = dx1*S, y = -dy1*S)
        
        # Move along the line
        T = 0.3
        # NORTH
        if direction == 1:
            if angle > 90:
                dx0 = (-np.cos((alpha * (np.pi/180))))*T
                dy0 = (np.sin((alpha * (np.pi/180))))*T
                vmx = int(dx0*500)
                vmy = -int(dy0*500)
                img = cv2.arrowedLine(img,(int(cx0), int(cy0)), (int(cx0 + vmx), int(cy0 + vmy)), (255,0,0), 5) # Volition marker
                m.move(x = dx0, y = dy0)
                
                if len(dir_x) > 5:
                    if abs(np.average(dir_x[-5:])) > abs(np.average(dir_y[-5:])):
                        direction = 4
                    elif abs(np.average(dir_x[-5:])) < abs(np.average(dir_y[-5:])):
                        direction = 1
            
            if angle < 90:
                dx0 = (np.cos((beta * (np.pi/180))))*T
                dy0 = (np.sin((beta * (np.pi/180))))*T
                vmx = int(dx0*500)
                vmy = -int(dy0*500)
                img = cv2.arrowedLine(img,(int(cx0), int(cy0)), (int(cx0 + vmx), int(cy0 + vmy)), (255,0,0), 5) # Volition marker
                m.move(x = dx0, y = dy0)
                
                if len(dir_x) > 5:
                    if abs(np.average(dir_x[-5:])) > abs(np.average(dir_y[-5:])):
                        direction = 2
                    elif abs(np.average(dir_x[-5:])) < abs(np.average(dir_y[-5:])):
                        direction = 1
        
        # EAST
        elif direction == 2:
            if angle > 90:
                dx0 = (np.cos((alpha * (np.pi/180))))*T
                dy0 = (-np.sin((alpha * (np.pi/180))))*T
                vmx = int(dx0*500)
                vmy = -int(dy0*500)
                img = cv2.arrowedLine(img,(int(cx0), int(cy0)), (int(cx0 + vmx), int(cy0 + vmy)), (255,0,0), 5) # Volition marker
                m.move(x = dx0, y = dy0)
                
                if len(dir_x) > 5:
                    if abs(np.average(dir_x[-5:])) > abs(np.average(dir_y[-5:])):
                        direction = 2
                    elif abs(np.average(dir_x[-5:])) < abs(np.average(dir_y[-5:])):
                        direction = 3
            
            if angle < 90:
                dx0 = (np.cos((beta * (np.pi/180))))*T
                dy0 = (np.sin((beta * (np.pi/180))))*T
                vmx = int(dx0*500)
                vmy = -int(dy0*500)
                img = cv2.arrowedLine(img,(int(cx0), int(cy0)), (int(cx0 + vmx), int(cy0 + vmy)), (255,0,0), 5) # Volition marker
                m.move(x = dx0, y = dy0)
                
                if len(dir_x) > 5:
                    if abs(np.average(dir_x[-5:])) > abs(np.average(dir_y[-5:])):
                        direction = 2
                    elif abs(np.average(dir_x[-5:])) < abs(np.average(dir_y[-5:])):
                        direction = 1
        
        # SOUTH
        elif direction == 3:
            if angle > 90:
                dx0 = (np.cos((alpha * (np.pi/180))))*T
                dy0 = (-np.sin((alpha * (np.pi/180))))*T
                vmx = int(dx0*500)
                vmy = -int(dy0*500)
                img = cv2.arrowedLine(img,(int(cx0), int(cy0)), (int(cx0 + vmx), int(cy0 + vmy)), (255,0,0), 5) # Volition marker
                m.move(x = dx0, y = dy0)
                
                if len(dir_x) > 5:
                    if abs(np.average(dir_x[-5:])) > abs(np.average(dir_y[-5:])):
                        direction = 2
                    elif abs(np.average(dir_x[-5:])) < abs(np.average(dir_y[-5:])):
                        direction = 3
            
            if angle < 90:
                dx0 = (-np.cos((beta * (np.pi/180))))*T
                dy0 = (-np.sin((beta * (np.pi/180))))*T
                vmx = int(dx0*500)
                vmy = -int(dy0*500)
                img = cv2.arrowedLine(img,(int(cx0), int(cy0)), (int(cx0 + vmx), int(cy0 + vmy)), (255,0,0), 5) # Volition marker
                m.move(x = dx0, y = dy0)
                
                if len(dir_x) > 5:
                    if abs(np.average(dir_x[-5:])) > abs(np.average(dir_y[-5:])):
                        direction = 4
                    elif abs(np.average(dir_x[-5:])) < abs(np.average(dir_y[-5:])):
                        direction = 3

        # WEST
        elif direction == 4:
            if angle > 90:
                dx0 = (-np.cos((alpha * (np.pi/180))))*T
                dy0 = (np.sin((alpha * (np.pi/180))))*T
                vmx = int(dx0*500)
                vmy = -int(dy0*500)
                img = cv2.arrowedLine(img,(int(cx0), int(cy0)), (int(cx0 + vmx), int(cy0 + vmy)), (255,0,0), 5) # Volition marker
                m.move(x = dx0, y = dy0)
                
                if len(dir_x) > 5:
                    if abs(np.average(dir_x[-5:])) > abs(np.average(dir_y[-5:])):
                        direction = 4
                    elif abs(np.average(dir_x[-5:])) < abs(np.average(dir_y[-5:])):
                        direction = 1
            
            if angle < 90:
                dx0 = (-np.cos((beta * (np.pi/180))))*T
                dy0 = (-np.sin((beta * (np.pi/180))))*T
                vmx = int(dx0*500)
                vmy = -int(dy0*500)
                img = cv2.arrowedLine(img,(int(cx0), int(cy0)), (int(cx0 + vmx), int(cy0 + vmy)), (255,0,0), 5) # Volition marker
                m.move(x = dx0, y = dy0)
                
                if len(dir_x) > 5:
                    if abs(np.average(dir_x[-5:])) > abs(np.average(dir_y[-5:])):
                        direction = 4
                    elif abs(np.average(dir_x[-5:])) < abs(np.average(dir_y[-5:])):
                        direction = 3
        
        # Image saving 
        cv2.imshow('Line Following Test', img)
        #time.sleep(0.25)
        #direct = 'C:/Users/University of Penn/Desktop/Video Capture/follow2/{:05}.png'.format(ct)
        #cv2.imwrite(direct, img)
        
        # Winding angle calculation
        if (dir_x[-1] != 0) and (dir_y[-1] != 0):
            x1 = dir_x[-1]
            y1 = dir_y[-1]
            x2 = dx0
            y2 = dy0
            dot = x1*x2 + y1*y2      # dot product
            det = x1*y2 - y1*x2      # determinant
            g = np.arctan2(det, dot)  # np.arctan2(y, x) or np.arctan2(sin, cos)
            gamma = gamma + g
        
        # Tracking path 
        dir_x.append(dx0)
        dir_y.append(dy0)
        xtr.append(xtr[-1]+dx0)
        ytr.append(ytr[-1]+dy0)
        
        if cv2.waitKey(1) & 0xFF == ord('q') or (abs(gamma) > 2*np.pi and abs(xtr[-1]) < 10 and abs(ytr[-1]) < 10):
            break 
        ct = ct + 1

    cv2.destroyAllWindows()
    m.close()
    
    # Cleanup
    ueye.is_StopLiveVideo(hcam, ueye.IS_FORCE_VIDEO_STOP)
    ueye.is_ExitCamera(hcam)
    plt.plot(xtr, ytr)
    
    return [xtr, ytr]
