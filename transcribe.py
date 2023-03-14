import whisper
import os
import tempfile
import shutil
import time

import sys
sys.path.insert(0, "C:\\projects\\.dependencies\\")
sys.path.insert(0, "C:\\projects\\.resources\\")

filetypes = (
	"cda",
	"mp3",
	"wav",
	"wma",
)
start = time.time()
print ("Loading model, please wait...")
model = whisper.load_model("medium")
end = time.time()
print("Model loaded in " + str(round((end-start)/60)) +'seconds.')


def transcribeFile(filename, outpath):
	print("Transcribing " + filename)
	start = time.time()
	transcription = model.transcribe(filename, language="fr", fp16=False)
	textlength = len(transcription["text"].split(' '))
	if textlength>5:
		print("Writing transcription of " +filename )
		with open(outpath, 'a', encoding='utf-8') as outfile:
			outfile.write(filename+'\n')
			outfile.write(transcription['text'])
			end = (time.time()-start)/60
			print("File transcribed in " + str(end))

DIR = input('Paste directory path here: ')

# Walk through all files in DIR including in subdirectories
# Find audio files and transcribe them, save resulting text file to Transcriptions folder
for subdir, dirs, files in os.walk(DIR):
	if subdir == "Transcriptions":
		continue
	for f in files:
		if f.lower().endswith(filetypes):
			outpath = DIR +"Transcriptions\\"+ f[:-4] + ".txt"
			if not os.path.isfile(outpath):
				transcribeFile(os.path.join(DIR, subdir, f), outpath)





