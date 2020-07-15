from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

face_classifier = cv2.CascadeClassifier(
    '/Users/jeremy/Documents/emotion_detection-master/haarcascade_frontalface_default.xml')
classifier = load_model('/Users/jeremy/Documents/emotion_detection-master/Emotion_little_vgg.h5')

class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']


def face_detector(img):
    # 转换图片格式
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return (0, 0, 0, 0), np.zeros((48, 48), np.uint8), img

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]

    try:
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
    except:
        return (x, w, y, h), np.zeros((48, 48), np.uint8), img
    return (x, w, y, h), roi_gray, img


cap = cv2.VideoCapture(0)

while True:
    # 捕获视频一帧
    ret, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        rect, face, image = face_detector(frame)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            # 根据ROI（region of interest感兴趣区域）预测表情结果
            preds = classifier.predict(roi)[0]
            label = class_labels[preds.argmax()]  # label就是表情结果字符串
            label_position = (x, y)
            # 显示结果到窗口里
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, 'No Face Found', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
    cv2.imshow('Emotion Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
