import whisper
import os
import tempfile
import shutil
import time

filetypes = (
	"cda",
	"mp3",
	"wav",
	"wma",
)
start = time.time()
print ("Loading model, please wait...")
model = whisper.load_model("medium")
print("Model loaded in " + str(round(time.time()-start)) +' seconds.')


def transcribeFile(filename, outpath):
	print("Transcribing " + filename)
	start = time.time()
	transcription = model.transcribe(filename, language="fr", fp16=False)
	textlength = len(transcription["text"].split(' '))
	if textlength>5:	#Dump any transcriptions of only a few words
		print("Writing transcription of " +filename )
		with open(outpath, 'a', encoding='utf-8') as outfile:
			outfile.write(filename+'\n')
			outfile.write(transcription['text'])
			print("File transcribed in " + str(round(time.time()-start)) +' seconds')

DIR = input('Paste directory path here: ')
os.mkdir(DIR + '//Transcriptions')

# Walk through all files in DIR including in subdirectories
# Find audio files and transcribe them, save resulting text file to Transcriptions folder
for subdir, dirs, files in os.walk(DIR):
	if subdir == "Transcriptions":
		continue
	for f in files:
		if f.lower().endswith(filetypes):
			outpath = DIR + '//Transcriptions//' + f[:-4] + ".txt"
			if not os.path.isfile(outpath):
				transcribeFile(os.path.join(DIR, subdir, f), outpath)





