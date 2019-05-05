# -*- coding: utf-8 -*-
"""
Purpose         : Speech recognition(Using Google API)
Created by      : Sathiya Raj Subburayan
Created date    : 4/21/2019

Other comments  : 
    
Required packages/modules   : conda install -c conda-forge speechrecognition

Modification history:
Date        Modified by         Modifications


"""

import speech_recognition as sr
#import numpy as np

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Please say something....")
    audio = r.listen(source)
try:
    print("You said: " + r.recognize_google(audio))
except Exception:
    print("Oops... Something went wrong")