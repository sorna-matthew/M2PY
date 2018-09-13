from pyueye import ueye
import numpy as np
import cv2
import time
 
def main():
    # init camera
    hcam = ueye.HIDS(0)
    ret = ueye.is_InitCamera(hcam, None)
    #print(f"initCamera returns {ret}")
 
    # set color mode
    ret = ueye.is_SetColorMode(hcam, ueye.IS_CM_BGR8_PACKED)
    #print(f"SetColorMode IS_CM_BGR8_PACKED returns {ret}")
    
    ueye.is_SetHWGainFactor(hcam, ueye.IS_SET_MASTER_GAIN_FACTOR, ueye.c_int(357))
    ret = ueye.is_SetHWGainFactor(hcam, ueye.IS_GET_MASTER_GAIN_FACTOR, ueye.c_int(100))
 
    # set region of interest
    width = 1280
    height = 1080
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
    ret = ueye.is_AllocImageMem(hcam, width, height, bitspixel,
                                mem_ptr, mem_id)
    #print(f"AllocImageMem returns {ret}")
     
    # set active memory region
    ret = ueye.is_SetImageMem(hcam, mem_ptr, mem_id)
    #print(f"SetImageMem returns {ret}")
 
    # continuous capture to memory
    ret = ueye.is_CaptureVideo(hcam, ueye.IS_DONT_WAIT)
    #print(f"CaptureVideo returns {ret}")
     
    # get data from camera and display
    lineinc = width * int((bitspixel + 7) / 8)
    
    time.sleep(1)
    
    ct = 0
    while True:
        img = ueye.get_data(mem_ptr, width, height, bitspixel, lineinc, copy=True)
        img_reshape = np.reshape(img, (height, width, 3))
        
        # Image Processing
        img_bgr = cv2.medianBlur(img_reshape, 35)
        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        bgr250  = np.uint8([[[72,31,165]]])
        hsv250 = cv2.cvtColor(bgr250,cv2.COLOR_BGR2HSV)
        lower = np.array([hsv250[0][0][0]-10, 100, 100])
        upper = np.array([hsv250[0][0][0]+10, 255, 255])
        mask = cv2.inRange(img_hsv, lower, upper)
        img = cv2.bitwise_and(img_reshape, img_reshape, mask= mask)
        
        wrdir = 'C:/Users/University of Penn/Desktop/Video Capture/nozzle_detect/{:05}.png'.format(ct)
        ct = ct + 1
        #cv2.imwrite(wrdir, img)
    
        cv2.imshow('uEye Python Example (q to exit)', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
     
    # cleanup
    ret = ueye.is_StopLiveVideo(hcam, ueye.IS_FORCE_VIDEO_STOP)
    #print(f"StopLiveVideo returns {ret}")
    ret = ueye.is_ExitCamera(hcam)
    print(f"ExitCamera returns {ret}")

if __name__ == '__main__':
    main()