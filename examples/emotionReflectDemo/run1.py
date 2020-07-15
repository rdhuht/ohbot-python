from ohbot import ohbot
from random import *
import threading
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

# 全局变量，控制移动和眨眼的开关
global moving, blinking

# 初始化不移动，不眨眼
moving = False
blinking = False

face_classifier = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml')
classifier = load_model('Emotion_little_vgg.h5')

# 检测表情分5类
class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']
global last_label, label
last_label = None
label = None


def blinkLids():
    global blinking

    # While True - Loop forever.
    while True:
        # if blinking is True.
        if blinking:
            # for the numbers 10 to 0 set the lidblink position. 
            for x in range(10, 0, -1):
                ohbot.move(ohbot.LIDBLINK, x)
                ohbot.wait(0.01)

            # for the numbers 0 to 10 set the lidblink position.
            for x in range(0, 10):
                ohbot.move(ohbot.LIDBLINK, x)
                ohbot.wait(0.01)

            # wait for a random amount of time for realistic blinking
            ohbot.wait(random() * 6)


# TODO 根据opencv检测的人脸位置，朝向那个方向, 方向可能是反的，需要测试
def lookatPerson(face_rect, windowSize):
    window_width, window_height = windowSize[2], windowSize[3]
    # print(window_width, window_height)  # 窗口的大小640，480
    x, w, y, h = face_rect
    middlex, middley = (x + w) / 2, (y + h) / 2
    headTurn, headNod = 2 * middlex / (window_width / 10), 2 * middley / (window_height / 10)
    if not (middlex == 0 or middley == 0):
        print(headTurn, headNod)
        # 0 - 160 - 320 - 480 - 640 x
        # 0                      10
        ohbot.move(ohbot.HEADTURN, headTurn)

        # 0 - 160 - 320 - 480 y
        # 0               10
        ohbot.move(ohbot.HEADNOD, headNod)



def randomLook():
    global moving
    while True:
        # if moving is True. 
        if moving:
            # Look in a random direction.
            ohbot.move(ohbot.EYETILT, randint(2, 8))
            ohbot.move(ohbot.EYETURN, randint(2, 8))

            # Wait for between 0 and 5 seconds. 
            ohbot.wait(random() * 5)


def randomTurn():
    global moving
    while True:
        if moving:
            # Move Ohbot's HEADTURN motor to a random position between 3 and 7.
            ohbot.move(ohbot.HEADTURN, randint(3, 7))

            # wait for a random amount of time before moving again. 
            ohbot.wait(random() * 4)


def randomNod():
    global moving
    while True:
        if moving:
            # Move Ohbot's HEADNOD motor to a random position between 4 and 7.
            ohbot.move(ohbot.HEADNOD, randint(4, 7))

            # wait for a random amount of time before moving again. 
            ohbot.wait(random() * 4)


def eyeCol():
    while True:
        # Set the base to a random rgb values between 0 and 10. 
        ohbot.setEyeColour(random() * 10, random() * 10, random() * 10)
        # Wait between 10 and 20 seconds before changing again. 
        ohbot.wait(randint(10, 20))


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
    # print(x, w, y, h)
    return (x, w, y, h), roi_gray, img


def emotion_reflect(label):
    global last_label
    try:
        if not label == last_label:
            if label == 'Angry':
                ohbot.say("angry")
            elif label == 'Happy':
                ohbot.say("happy")
            elif label == 'Neutral':
                ohbot.say("neutral")
            elif label == 'Sad':
                ohbot.say('sad')
            elif label == 'Surprise':
                ohbot.say("surprised")
            elif label == "No Face Found!":
                ohbot.say("look at me!")
            last_label = label
    except:
        print("label failed")


# 重置ohbot
ohbot.reset()
ohbot.wait(1)

# 打开移动和眨眼
moving = True
blinking = True

# 打开摄像头
cap = cv2.VideoCapture(0)

# 创建眨眼线程
t1 = threading.Thread(target=blinkLids, args=())

# 创建四处看线程
t2 = threading.Thread(target=randomLook, args=())

# 创建随机点头线程
t3 = threading.Thread(target=randomNod, args=())

# 创建随机转头线程
t4 = threading.Thread(target=randomTurn, args=())

# 创建眼睛随机颜色线程
t5 = threading.Thread(target=eyeCol, args=())

# 启动所有线程
t1.start()
# t2.start()
# t3.start()
# t4.start()
# t5.start()


ohbot.say("hello")

while True:
    # 捕获视频
    ret, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        rect, face, image = face_detector(frame)
        lookatPerson(rect, windowSize)
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
            label = "No Face Found!"
    cv2.imshow('Emotion Detector', frame)
    windowSize = cv2.getWindowImageRect("Emotion Detector")
    emotion_reflect(label)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
