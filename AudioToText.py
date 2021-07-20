import speech_recognition as sr
file_name = "Soap-extract23.wav"
filename = "./Extracts/"+file_name
r = sr.Recognizer()

print("\n\n\nText Extracted from Audio File {} is : \n\n".format(filename))
audio = sr.AudioFile(filename)
with audio as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)
f = open("TextGen.txt", "a")
f.write("\t"+file_name)
f.write("\n\n"+text+"\n\n\n\n\n")
f.close()
