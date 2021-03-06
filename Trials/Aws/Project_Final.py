import pandas as pd
import numpy as np
import keras
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import h5py

import shutil

from keras.layers import Flatten, Dense, Input, concatenate
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout
from keras.models import Model
from keras.models import Sequential


import cv2
import os
import time
from PIL import Image, ImageStat
from scipy.spatial import distance

from PIL import Image


import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from nltk.translate.bleu_score import sentence_bleu
from heapq import nlargest

t1 = time.time()

Marker = [0]


def calculate_similarity(vector1, vector2):
    return (1 - distance.cosine(vector1, vector2))


def get_feature_vector(img):
    img1 = cv2.resize(img, (224, 224))
    feature_vector = basemodel.predict(img1.reshape(1, 224, 224, 3))
    return feature_vector


vgg16 = keras.applications.VGG16(
    weights='imagenet', include_top=True, pooling='max', input_shape=(224, 224, 3))


basemodel = Model(inputs=vgg16.input, outputs=vgg16.get_layer('fc2').output)
print(basemodel.summary())


try:
    dirPath = './data'
    if(os.path.exists(dirPath)):
        shutil.rmtree(dirPath)
        # print("Deleted ",dirPath)
        os.mkdir(dirPath)
except:
    print('Error while Deleing or Creating directory', dirPath)
if not os.path.exists('data'):
    os.makedirs('data')

file_name = "Aws"
ext = ".mp4"

vidcap = cv2.VideoCapture(file_name+ext)
prev = 0

sec = 0
frameRate = 5
count = 0
chosen = 1
vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
hasFrames, prev = vidcap.read()

if not os.path.exists('temp'):
    os.makedirs('temp')
cv2.imwrite('./temp/prev.jpg', prev)

# prevImage = Image.open(r'./temp/prev.jpg')
# print("Type: ", type(prev))
while hasFrames:
    count = count + 1
    sec = sec + frameRate
    # sec = round(sec, 2)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
    hasFrames, current = vidcap.read()

    if (hasFrames):
        cv2.imwrite("./temp/current.jpg", current)
        # currentImage = Image.open(r"./temp/current.jpg")
        # if hasFrames:

        image1 = cv2.imread("./temp/prev.jpg")
        image2 = cv2.imread("./temp/current.jpg")

        f1 = get_feature_vector(image1)
        f2 = get_feature_vector(image2)

        # print("\n\nSimilarity : {}\n\n\n\n".format(
        similarity = calculate_similarity(f1, f2)
        print("\n\nCapture{} : Similarity = {}".format(count, similarity))

        if(similarity < 0.9):
            name = './data/frame' + str(chosen) + '.jpg'
            print('______ Creating... frame{} ______'.format(chosen))
            cv2.imwrite(name, prev)    # save frame as JPG file
            chosen += 1
            prev = current.copy()
            cv2.imwrite("./temp/prev.jpg", current)
            Marker.append(count*5)
            # print("\n\n\n Current: ", type(current))
            # print("\n\n\n Current Image: ", type(currentImage))
            # prevImage = currentImage


name = './data/frame' + str(chosen) + '.jpg'
print('______ Creating... frame{}______ '.format(chosen))

cv2.imwrite(name, prev)
Marker.append((count+1)*5)

# save frame as JPG file
# print("Total Distinct Images Generated : ", count+1)
# print("\n\n\n Current: ", type(current))
# print("\n\n\n Current Image: ", type(currentImage))
t2 = time.time()-t1
minutes = int(t2//60)
seconds = int(t2 % 60)
print("\n\n\n_______ Elapsed Time:    {} min : {} sec _______\n\n".format(
    minutes, seconds))
print("Images Generated: ", count+1)
print("Images Selected: ", chosen+1, "\n\n")
print("Markers for Segmentation  : ", Marker)


# ================================================================================================================================
# Save pdf

def getPDF(output_name):
    folder_name = "data"
    folder_address = "./"+folder_name
    name_list = os.listdir(folder_address)

    image = Image.open(folder_address+"/"+name_list[0])
    first_image = image.convert('RGB')

    image_list = []
    for i in range(1, len(name_list)):
        image = Image.open(folder_address+"/"+name_list[i])
        img = image.convert('RGB')
        image_list.append(img)

    first_image.save(output_name+".pdf", save_all=True,
                     append_images=image_list)


getPDF(file_name)

# ==================================================================================================================================


def getAudioChunks(Marker, file_name):

    try:
        dirPath = './Extracts'
        if(os.path.exists(dirPath)):
            shutil.rmtree(dirPath)
            # print("Deleted ",dirPath)
            os.mkdir(dirPath)
    except:
        print('Error while Deleing or Creating directory', dirPath)
    # Taking input file
    files_path = os.getcwd()+"\\"

    clip = mp.VideoFileClip(r""+file_name+'.mp4')
    clip.audio.write_audiofile(r""+file_name+'.wav')
    print("\n\n\n_____ Converted to mp3 _____\n\n\n")
    song = AudioSegment.from_mp3(files_path+file_name+'.wav')

    # time point based on sec hardcoded

    # Folder for Extracts
    folder_name = files_path+"Extracts\\"

    whole_text = ""

    for mark in range(len(Marker)-1):
        startMin = 0
        startSec = Marker[mark]
        endMin = 0
        endSec = Marker[mark+1]
        startTime = startMin*60*1000+startSec*1000
        endTime = endMin*60*1000+endSec*1000
        extract = song[startTime:endTime]
        print('\n______ Creating Audio-Extract: {}______ '.format(mark+1))
        extract.export(folder_name+file_name+'-extract' +
                       str(mark+1) + '.wav', format="wav")

    print("\n\n\n_______ Total files Extracted : ", mark+1, " _______\n\n\n\n")


print("\n\n\n\n<<<<<<<<< Video to Audio-Segmentation based on Markers >>>>>>>>>> \n\n")
getAudioChunks(Marker, file_name)

# ==============================================================================================
Trans_List = []


def getTranscript(Marker, file_name):
    global Trans_List
    try:
        dirPath = './Transcripts'
        if(os.path.exists(dirPath)):
            shutil.rmtree(dirPath)
            # print("Deleted ",dirPath)
            os.mkdir(dirPath)
    except:
        print('Error while Deleing or Creating directory', dirPath)
    Entire_text = ""
    Trans_Folder = "Transcripts"
    files_path = os.getcwd()+"\\"
    folder_name = files_path+Trans_Folder+"\\"
    # if not os.path.isdir(folder_name):
    #     os.mkdir(folder_name)

    for i in range(len(Marker)-1):
        Aud_Chunk_name = "./Extracts/"+file_name+"-extract"+str(i+1)+".wav"
        r = sr.Recognizer()

        n = len(AudioSegment.from_wav(Aud_Chunk_name))
        seconds = n/1000
        minutes = int(seconds//60)
        seconds = int(seconds % 60)
        print("\n\n\n\nFile{}".format(Aud_Chunk_name))
        print("  Length    {} min : {} sec ".format(minutes, seconds))
        maxdur = 5*60*1000
        start = 0
        end = 0
        text = ""
        print("\nText-Extracted : ")
        audio = sr.AudioFile(Aud_Chunk_name)
        with audio as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            while(end < n):
                audio_data = r.record(source, duration=maxdur//1000)
                end += maxdur
                try:
                    text = text + " " + r.recognize_google(audio_data)

                    # f = open("TextGen.txt", "a")
                    # f.write("\t"+file_name)
                    # f.write("\n\n"+text+"\n\n\n\n\n")
                    # f.close()

                except sr.RequestError as e:
                    print("Error:", str(e))

                except sr.UnknownValueError as e:
                    print("Error:", str(e))
            print(text)

        Trans_List.append(text)
        Entire_text += (text+" . ")
        f = open("./Transcripts/"+file_name+"-trans" + str(i+1) + ".txt", "w")
        f.write(text)
        f.close()

    Trans_List.append(Entire_text)
    f = open("./Transcripts/"+file_name+"-Transcript" + ".txt", "w")
    f.write(Entire_text)
    f.close()
    print("\n\n\n _______ Entire Transcript is _______\n\n", Entire_text)


print(Marker)
getTranscript(Marker, file_name)


# T5
def getT5Summary(text):
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    preprocess_text = text.strip().replace("\n", "")
    t5_prepared_Text = "summarize: "+preprocess_text
    tokenized_text = tokenizer.encode(
        t5_prepared_Text, return_tensors="pt")
    summary_ids = model.generate(tokenized_text,
                                 num_beams=4,
                                 no_repeat_ngram_size=2,
                                 min_length=30,
                                 max_length=100,
                                 early_stopping=True)

    T5_Summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("Summary using T5 Model : \n\n", T5_Summary, "\n\n")
    return T5_Summary


def getNLPSummary(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for token in doc]
    stopwords = list(STOP_WORDS)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens)*0.3)
    summary1 = nlargest(select_length, sentence_scores,
                        key=sentence_scores.get)

    NLP_Summary = ""
    for s in summary1:
        NLP_Summary = NLP_Summary+s.text
    print("\nSummary using NLP :\n\n", NLP_Summary, "\n\n")
    return NLP_Summary

# =======================================================================================================================================


def getSummary(text):
    l = text.split()
    if(len(l) < 50):
        Final_Summary = text
        print("\n\nFinal Summary is :\n\n",
              Final_Summary, "\n\n")

    else:
        T5_Summary = getT5Summary(text)
        NLP_Summary = getNLPSummary(text)

        # Bleu Score
        reference = T5_Summary.split(" ")
        candidate = NLP_Summary.split(" ")

        score = sentence_bleu(reference, candidate)
        print("\nThe Blue score is {}".format(score))

        if(score < 0.5):
            Final_Summary = T5_Summary+NLP_Summary
            print("\n\n==========  Final = T5 + NLP  ==========")
        else:
            Final_Summary = T5_Summary
            print("\n\n==========  Final = T5  ==========")

        Final_Summary = T5_Summary
        print("\n\nFinal Summary using Bleu Score is :\n\n",
              Final_Summary, "\n\n")
    return Final_Summary


try:
    dirPath = './Summary'
    if(os.path.exists(dirPath)):
        shutil.rmtree(dirPath)
        # print("Deleted ",dirPath)
        os.mkdir(dirPath)
except:
    print('Error while Deleing or Creating directory', dirPath)

Summ_Folder = "Summary"
files_path = os.getcwd()+"\\"
folder_name = files_path+Summ_Folder+"\\"


Trans_Folder = "Transcripts"
folder_address = "./"+Trans_Folder
name_list = os.listdir(folder_address)
choice = 0
# print("\n\n\n\n You can give choice for Summarizer : \n 0. Both Part by and whole Summary\n 1. Part Summary only\n 2. Whole Summary only\n\n")
# choice = int(input("\n\n\n______ Enter choice for summary : "))

if(choice == 0 or choice == 1):
    for i in range(len(name_list)-1):
        # file = open(folder_address+"/"+name_list[i], "r")
        # text = file.read()
        text = Trans_List[i]
        # file.close
        print("\n\n\n  ========= Summary File : {} ========\n".format(
            file_name + "-summ" + str(i+1) + ".txt"))
        Final_Summary = getSummary(text)

        f = open("./"+Summ_Folder+"/"+file_name +
                 "-summ" + str(i+1) + ".txt", "w")
        f.write(Final_Summary)
        f.close()

if(choice == 0 or choice == 2):
    # file = open(folder_address+"/"+name_list[-1], "r")
    # text = file.read()
    text = Trans_List[-1]
    # file.close
    print("\n\n\n  ========= Summary File : {} ========\n".format(
        file_name + "-Summary" + ".txt"))

    Final_Summary = getSummary(text)

    f = open("./"+Summ_Folder+"/"+file_name+"-Summary" + ".txt", "w")
    f.write(Final_Summary)
    f.close()
