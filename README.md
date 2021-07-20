# Visual-and-Texual-Summary-Generator-from-Video
It will prepare a summary from the speech identified from video as well as give you ready made pdf of all the slides shown in Video :) 

Phases involved in the project are : 
- Phase 1: key frames extraction using deep learning model VGG16.
- Phase 2: Video to audio, audio to text generation based on time between key frames.
- Phase 3: Combined summary generation from text using a) T5 model for abstractive Summary. b) NLP for extractive Summary.


To run the project :
1) Put the input video in the Downloaded Folder
2) Set input to the filename 
3) Run main.py , this will generate all the files in the directory.
4) Run GUI.py, to view the final visual and texual summary in the form of GUI
