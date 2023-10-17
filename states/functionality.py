import numpy as np
import winsound
import speech_recognition as sr

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
#from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

API_KEY = "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"
chat = ChatOpenAI(openai_api_key=API_KEY, model_name="gpt-3.5-turbo", temperature=0.9)


def faceDetectionHandler_check_for_face(stateData):
    
    
    timeToShowFace = 3
    start = np.datetime64('now')
    
    while (np.datetime64('now') < start + np.timedelta64(timeToShowFace, "s")):
        data = stateData.get()
        
        
        if len(data["faces"]) > 0:
            winsound.PlaySound("tts_sentences/found_you.wav", winsound.SND_FILENAME)
            stateData.wait(2)
            winsound.PlaySound("tts_sentences/processing_face.wav", winsound.SND_FILENAME)
            return True
            
    return False


def faceDetectionHandler_recognized_face(stateData):
    
    
    timeToRecognizeFace = 10
    start = np.datetime64('now')
    
    while (np.datetime64('now') < start + np.timedelta64(timeToRecognizeFace, "s")):
        data = stateData.get()
        
        
        for face in data["faces"].values():
            if face.label not in [None, -1]:
                
                return True
            
    winsound.PlaySound("tts_sentences/face_not_recognized.wav", winsound.SND_FILENAME)
    return False



def general_speech_detection():
    
    with sr.Microphone() as source:
        winsound.Beep(1000,100)
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = False
        recognizer.energy_threshold = 500
        return recognizer.listen(source,phrase_time_limit=5)
    
def processPasswordHandler_lang_setup(username):
    
    if username == "human":
        system_message = "You are a guard robot named Hubert with the purpose of surveilling Area 51. " \
                         "You are talking to a {user} who is authorized personnel. " \
                         "The conversation started by you asking the {user} how they are doing. " \
                         "You always answer in English regardless of what language a question was told."
    else:
        system_message = "You are a guard robot named Hubert with the purpose of surveilling Area 51. " \
                         "You are talking to {user} who is authorized personnel. " \
                         "The conversation started by you asking {user} how they are doing. " \
                         "You always answer in English regardless of what language a question was told."

    prompt = ChatPromptTemplate(
        input_variables=['user', 'chat_history', 'question'],
        messages=[
            SystemMessagePromptTemplate.from_template(system_message),
            # The `variable_name` here is what must align with memory
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key='question', return_messages=True)

    conv_chain = LLMChain(
        llm=chat,
        prompt=prompt,
        memory=memory
    )
    
    return conv_chain
    
def processPasswordHandler_get_username(stateData):

    username = "human" #a human
    data = stateData.get()
    faces = list(data["faces"].values())
    if (len(faces) != 0):
        print("entry Approved handler NAME:", faces[0].label)
        if faces[0].label not in [-1, None]:
            username = faces[0].label
            
            
def defendHandler_pearson_has_left(stateData):
    timeToLeave = 20
    start = np.datetime64('now')
    
    while (np.datetime64('now') < start + np.timedelta64(timeToLeave, "s")):

        data = stateData.get()
        faces = list(data["faces"].values())
        bodyPos = stateData.position["B"]
        if bodyPos > 2200 or bodyPos < 700:
            return True
        
        elif len(faces) == 0:
            return True
        
        
def defendHandler_shoot_sound():
    
    winsound.PlaySound("tts_sounds/blaster.wav", winsound.SND_FILENAME)
   
    