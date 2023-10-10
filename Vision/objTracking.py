import cv2
import numpy as np
#Code from https://mpolinowski.github.io/docs/IoT-and-Machine-Learning/ML/2021-12-10--opencv-optical-flow-tracking/2021-12-10/
vid = cv2.VideoCapture(0)
# get first video frame
ok, frame = vid.read()
def object_tracking(faceCoords, queue, terminate):
    frame_gray_init = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #edges = cv2.goodFeaturesToTrack(frame_gray_init, mask = None, **parameters_shitomasi)
    #print(edges)
    old_points = np.array([faceCoords], dtype=np.float32)
    # create a black canvas the size of the initial frame
    canvas = np.zeros_like(frame)
    # create random colours for visualization for all 100 max corners for RGB channels
    #colours = np.random.randint(0, 255, (100, 3))
    # set min size of tracked object, e.g. 15x15px
    parameter_lucas_kanade = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    while True:
        # get next frame
        ok, frame = vid.read()
        if not ok:
            print("[ERROR] reached end of file")
            break
        # covert to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.circle(frame, old_points, 5, (0, 0, 255), 2)
        # update object corners by comparing with found edges in initial frame
        new_points, status, errors = cv2.calcOpticalFlowPyrLK(frame_gray_init, frame_gray, faceCoords, None,
                                                            **parameter_lucas_kanade)

        # overwrite initial frame with current before restarting the loop
        frame_gray_init = frame_gray.copy()
        # update to new edges before restarting the loop
        old_points = new_points

        x, y = new_points.ravel()
        j, k = old_points.ravel()

        # draw line between old and new corner point with random colour
        # canvas = cv2.line(canvas, (int(x), int(y)), (int(j), int(k)), (0, 255, 0), 3)
        # draw circle around new position
        #frame = cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)

        result = cv2.add(frame, canvas)
        cv2.imshow('Optical Flow', result)
        if terminate == 0:
            break
        while queue.full():
            queue.get()
        queue.put(old_points)
