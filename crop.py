import cv2 
import datetime

original = cv2.imread('united.jpeg')                 # read image
resized_original = cv2.resize(original, (800,800))   # resize it
temp = resized_original.copy()                       # make a temporary copy of it                   

prevX = 0
prevY = 0 
currentX = 0
currentY = 0

def callback(event, x, y, flag, param):
    global prevX,prevY,temp,currentX,currentY

    if event == cv2.EVENT_LBUTTONDOWN:
        prevX = x
        prevY = y
        
    elif event == cv2.EVENT_MOUSEMOVE and flag == cv2.EVENT_FLAG_LBUTTON:
        temp = resized_original.copy() # <---------------------------------- IMPORTANT
        currentX = x
        currentY = y
        cv2.rectangle(temp, (prevX,prevY), (x,y), (0,255,0), 3)

# not exactly required, but lets you drag the cropping rectangle in all directions
# instead of just top left to bottom right.

def selectROI(): 
    if prevX < currentX and prevY < currentY:
        return resized_original[ prevY:currentY , prevX:currentX , : ]

    elif prevX > currentX and prevY < currentY:
        return resized_original[ prevY:currentY , currentX:prevX , : ]

    elif prevX < currentX and prevY > currentY:
        return resized_original[ currentY:prevY , prevX:currentX , : ]

    elif prevX > currentX and prevY > currentY:
        return resized_original[ currentY:prevY , currentX:prevX , : ]


cv2.namedWindow('picture')
cv2.setMouseCallback('picture', callback)   # set callback yay!

while True:

    cv2.imshow('picture', temp)  # show the temporary copy of the resized original 
    ret = cv2.waitKey(1)    
    
    if ret == -1:
        continue
    
    elif ret == 27:           # press esc to quit
        break
    
    elif ret == ord('c'):    # press c to crop once rectangle is drawn
        
        cropped_image = selectROI()       
        print('confirm crop? y/n')             # press y/n to confirm the crop 
        cv2.imshow('crop', cropped_image)
        choice = cv2.waitKey(0)

        if choice == ord('y'):
           
            now = datetime.datetime.now()
            timeStamp = now.strftime("%d-%m-%Y_%H:%M:%S")
            name = 'cropped_'+timeStamp+'.jpeg'
            print('saved as ',name)
            cv2.imwrite(name, cropped_image)

        cv2.destroyWindow('crop')

cv2.destroyAllWindows()
