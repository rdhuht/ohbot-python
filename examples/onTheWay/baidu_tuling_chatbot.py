from aip import AipSpeech
import requests
import json
import speech_recognition as sr
import ohbot


# 初始化语音
# ohbot.say('Hello')

# 语音生成音频文件,录音并以当前时间戳保存到voices文件中
# Use SpeechRecognition to record 使用语音识别录制
def my_record():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("please say something")
        print('Listening')
        audio = r.listen(source)
    with open("/Users/jeremy/Documents/GitHub/ohbot-python/examples/OntheWay/voices/myvoices.wav", "wb") as f:
        f.write(audio.get_wav_data())


# 音频文件转文字：采用百度的语音识别python-SDK
# 导入我们需要的模块名，然后将音频文件发送给出去，返回文字。
# 百度语音识别API配置参数
# TODO 账号过期了
APP_ID = '16804924'
API_KEY = 'ltMeA25QHGmbouj5wt05obPv'
SECRET_KEY = 'GPZyYUacr5G1g3SVouBbkBx7f9VQzdsA'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
path = '/Users/jeremy/Documents/GitHub/ohbot-python/examples/OntheWay/voices/myvoices.wav'


# 将语音转文本STT
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def listen():
    # 读取录音文件
    try:
        # 识别本地文件
        result = client.asr(get_file_content(path), 'wav', 16000, {'dev_pid': 1537, })
        print(result)
        return result  # result需要进一步解析
    except KeyError:
        # print("KeyError")
        print("我没有听清楚，请再说一遍...")


# 与机器人对话：调用的是图灵机器人
# 图灵机器人的API_KEY、API_URL
# TODO 需要购买账号
turing_api_key = "your turing_api_key"
api_url = "http://openapi.tuling123.com/openapi/api/v2"  # 图灵机器人api网址
headers = {'Content-Type': 'application/json;charset=UTF-8'}


# 图灵机器人回复
def Turing(text_words=""):
    req = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": text_words
            },

            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": "崔各庄"
                }
            }
        },
        "userInfo": {
            "apiKey": turing_api_key,  # 你的图灵机器人apiKey
            "userId": "Nieson"  # 用户唯一标识(随便填, 非密钥)
        }
    }

    req["perception"]["inputText"]["text"] = text_words
    response = requests.request("post", api_url, json=req, headers=headers)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("AI Robot said: " + result)
    return result


# 语音合成，输出机器人的回答
while True:
    my_record()  # 录音成功
    request = listen()  # 百度aip账号过期
    # response = Turing(request)  # 图灵账号购买
