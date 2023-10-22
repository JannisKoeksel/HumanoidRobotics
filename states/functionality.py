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
    """
    Detects a face within a 3-second window. If detected, plays associated sound files.
    
    Parameters:
    - stateData (StateData): An instance of the StateData class which provides methods for fetching data, moving parts, and following detected objects.

    Returns:
    - bool: True if a face is detected within the time window, otherwise False.
    """

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
    """
    Checks for a recognized face within a 10-second window. If not recognized, plays an associated sound file.
    
    Parameters:
    - stateData (StateData): An instance of the StateData class which provides methods for fetching data, moving parts, and following detected objects.

    Returns:
    - bool: True if a face with a recognized label is detected within the time window, otherwise False (and plays a "not recognized" sound).
    """
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
    """
    Captures a speech snippet using the microphone for up to 5 seconds after beeping. 
    
    Returns:
    - AudioData: An object containing captured audio data.
    """
    
    with sr.Microphone() as source:
        winsound.Beep(1000,100)
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = False
        recognizer.energy_threshold = 500
        return recognizer.listen(source,phrase_time_limit=5)
    
def processPasswordHandler_lang_setup(username):
    """
    Sets up a conversation chain for a guard robot named Hubert in Area 51. The conversation context is
    determined by the `username` provided, with specific messaging for the user named "human".
    
    Parameters:
    - username (str): The name of the user. Special messaging is set if username is "human".
    
    Returns:
    - LLMChain: An LLMChain object containing conversation prompt and memory configurations for the chat.
    """
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
    """
    Retrieves the username based on the recognized face label from the provided state data.
    If no recognized face is detected, defaults to "human".
    
    Parameters:
    - stateData (StateData): An instance of the StateData class which provides methods for fetching data, moving parts, and following detected objects.
    
    Returns:
    - str: Recognized username or "human" if no recognized face is detected.
    """
    username = "human" #a human
    data = stateData.get()
    faces = list(data["faces"].values())
    if (len(faces) != 0):
        
        for face in faces: 
            if face.label not in [-1, None]:
                return face.label
            
    return username
        
def defendHandler_pearson_has_left(stateData):
    """
    Monitors for Pearson's exit within a 20-second window by leveraging the functionalities of the StateData class. Pearson's exit is determined either by not detecting any faces or based on body position thresholds.

    Parameters:
    - stateData (StateData): An instance of the StateData class which provides methods for fetching data, moving parts, and following detected objects.

    Returns:
    - bool: True if Pearson has left (based on face count or body position criteria). If neither criteria is met within the time window, the function ends without a return value.
    """

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
    """
    Plays a warning sound followed by a blaster sound using the winsound library.

    Returns:
    - None
    """
    winsound.PlaySound("tts_sentences/your_time_is_up.wav", winsound.SND_FILENAME)
    winsound.PlaySound("tts_sounds/blaster.wav", winsound.SND_FILENAME)
   
    