import time





def face_detection(queue, terminate):
    from ultralytics import YOLO
    import cv2
    model = YOLO("Vision\Models\yolov8n-face.pt")
    vid = cv2.VideoCapture(0)
    ret, img = vid.read()
    results = model(img)
    
    
    
    centerImage = [320,240]
    frameWidth  = 10000  # float `width`
    frameHeight = 10000
    facePadding = 0
    
    while (True):
        #Image path to the test picture
        #img_path = "FaceTest.jpg"
        #Apply model on the image and saves the results (Coordinates for rectangles)
        ret, img = vid.read()

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if terminate.value == 1:
            break
        
        
        results = model(img, verbose=False)
        #Info about the detected faces are found in boxes.
        boxes = results[0].boxes

        #Saves coordinates for the boxes and adds them onto the image
        faceImage = []
        faceCoordinates = []
       
        
        for box in boxes:
            #Extracting coordinates of detected faces
            top = int(box.xyxy.tolist()[0][0])
            left = int(box.xyxy.tolist()[0][1])
            bottom = int(box.xyxy.tolist()[0][2])
            right = int(box.xyxy.tolist()[0][3])
            
            #Send the difference between the center of the rectangle encapsulating the first face and the center of the image 
            #to Arduino with a scale factor, should make the robot track the faces. However, may have to make it so it only 
            #sends it to Arduino every X frames so it doesn't have a seizure, also scale factor could be important.
            leftP = max(left-facePadding,0)
            topP = max(top-facePadding,0)
            rightP = min(right+facePadding,frameWidth)
            bottomP =  min(bottom+facePadding,frameHeight)
            
            faceImage.append(img[leftP:rightP, topP:bottomP])
            faceCoordinates.append([leftP,topP,rightP,bottomP])
            
            # cv2.rectangle(img,(top, left), (bottom, right),(255,0,0),2)
            
            
        queue_data = {
            "frame": img,
            "faces": faceCoordinates
        }
        
       
        queue.put(queue_data)
        time.sleep(0.01)
        
    # Cleanup
    vid.release()

    exit(0)