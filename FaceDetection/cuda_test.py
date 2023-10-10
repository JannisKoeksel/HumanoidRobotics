import dlib
dlib.DLIB_USE_CUDA = True
dlib.cuda.set_device(0)
import face_recognition
import numpy as np
import face_recognition_models

# import cv2
# video_capture = cv2.VideoCapture(0)
jannis_image = face_recognition.load_image_file("D:/IT/HumanoidRobotics/FaceDetection/faces/jannis.jpg")





predictor_5_point_model = face_recognition_models.pose_predictor_five_point_model_location()
pose_predictor_5_point = dlib.shape_predictor(predictor_5_point_model)

cnn_face_detection_model = face_recognition_models.cnn_face_detector_model_location()
cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_face_detection_model)

face_recognition_model = face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)
img = jannis_image
print("run")
pose_predictor = pose_predictor_5_point
num_jitters = 1
face_locations = cnn_face_detector(img, 0)
print(face_locations)
raw_landmarks = [pose_predictor(img, face_location) for face_location in face_locations]
exit()
faces =  [np.array(face_encoder.compute_face_descriptor(jannis_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]

print(faces)