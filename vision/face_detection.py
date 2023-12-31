import time
import traceback




def face_detection(queue, terminate):
    """
    Real-time face detection using a webcam and YOLO from the ultralytics library.

    This function captures frames from the webcam, applies the YOLO model to detect faces,
    and pushes the frames along with the detected face coordinates to the provided queue. 
    The detection runs continuously until the `terminate` flag is set.

    Parameters:
    - queue (multiprocessing.Queue): A queue to push the frames and detected face coordinates.
    - terminate (multiprocessing.Value): A flag to control the termination of the detection loop.
        If set to 1, the detection stops.

    Outputs to queue:
    - frame (numpy.ndarray): The captured frame from the webcam.
    - faces (list): List of coordinates of detected faces in the format [left, top, right, bottom].

    Note:
    Ensure that the terminate flag is initialized to 0 for the function to start. To stop the function,
    set the terminate flag to 1. The provided queue should be used to retrieve the frames and face data
    in another process.

    Returns:
    None

    Raises:
    Exception: If there's an error during the detection or capturing process.
    """
    from ultralytics import YOLO
    import cv2
    model = YOLO("Vision\Models\yolov8n-face.pt")
    #Start recording, outside of for loop since first iteration will use CPU and will therefore be slow.
    vid = cv2.VideoCapture(0)
    ret, img = vid.read()
    #Extracting results
    results = model(img)
    
    
    
    centerImage = [320,240]
    frameWidth  = 10000  # float `width`
    frameHeight = 10000
    facePadding = 0
    try:
        while (True):
            #Image path to the test picture
            #img_path = "FaceTest.jpg"
            #Apply model on the image and saves the results (Coordinates for rectangles)
            #Extracts frame and OK condition
            ret, img = vid.read()
            if( not ret):
                print("Frame capture failed")
                continue
            #Terminates the function
            if terminate.value == 1:
                break
            
            #Applies model on iamge and extracts result, verbose=false to skip all the print messages
            results = model(img, verbose=False)
            #Info about the detected faces are found in boxes.
            boxes = results[0].boxes

            #Initializes vectors that will be sent to the queue 
            faceImage = []
            faceCoordinates = []
        
            #Loop through every "box(=face)"
            for box in boxes:
                #Extracting coordinates of detected faces
                top = int(box.xyxy.tolist()[0][0])
                left = int(box.xyxy.tolist()[0][1])
                bottom = int(box.xyxy.tolist()[0][2])
                right = int(box.xyxy.tolist()[0][3])
                
                #Adds padding to the face, so that the images can easier be used for recognition
                leftP = max(left-facePadding,0)
                topP = max(top-facePadding,0)
                rightP = min(right+facePadding,frameWidth)
                bottomP =  min(bottom+facePadding,frameHeight)

                #Appends the necessary information to vectors
                faceImage.append(img[leftP:rightP, topP:bottomP])
                faceCoordinates.append([leftP,topP,rightP,bottomP])
                
                # cv2.rectangle(img,(top, left), (bottom, right),(255,0,0),2)
                
            #Sends the image and face coordinates to the queue
            queue_data = {
                "frame": img,
                "faces": faceCoordinates
            }
            
        
            queue.put(queue_data)
            time.sleep(0.01)
    except Exception as e:
        print("detection",e)
        print(traceback.format_exc())
    # Cleanup
    vid.release()

  