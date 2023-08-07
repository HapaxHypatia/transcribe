import whisper
import os
import tempfile
import shutil
import time
import tkinter as tk
from tkinter import simpledialog

def getFile():
	ROOT = tk.Tk()
	ROOT.withdraw()
	# # the input dialog
	USER_INP = simpledialog.askstring(title="filepath",
                                  prompt="Path to your audio file:")
	return USER_INP


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


def transcribeFile(filename, destDIR):
	print("Transcribing " + filename)
	if not os.path.isdir(destDIR + '//Transcriptions'):
		os.mkdir(destDIR + '//Transcriptions')
	start = time.time()
	transcription = model.transcribe(filename, language="fr", fp16=False)
	textlength = len(transcription["text"].split(' '))
	if textlength>5:	#Dump any transcriptions of only a few words
		file_stats = os.stat(filename)
		name = os.path.splitext(os.path.basename(filename))[0]
		log = open('logs.txt', 'a', encoding='utf-8')
		log.write(name)
		log.write("\n\n")
		log.write("Size: {}mb.".format(file_stats.st_size / (1024 * 1024)))
		log.write("\n\n")
		print("Writing transcription of " +name )
		#Create transcriptions folder in specified directory
		outpath = destDIR + '//Transcriptions//' + name + ".txt"
		with open(outpath, 'a', encoding='utf-8') as outfile:
			outfile.write(name+'\n')
			outfile.write(transcription['text'])
			log.write("File transcribed in " + str(round(time.time()-start)) +' seconds')
			log.write("\n\n")

def transcribeDIR(DIR):
	# Walk through all files in DIR including in subdirectories
	# Find audio files and transcribe them, save resulting text file to Transcriptions folder
	for subdir, dirs, files in os.walk(DIR):
		if subdir == "Transcriptions":
			continue
		for f in files:
			outpath = destDIR + '//Transcriptions//' + f[:-4] + ".txt"
			if f.lower().endswith(filetypes):
				if not os.path.isfile(outpath):
					transcribeFile(os.path.join(DIR, subdir, f), DIR)


if __name__ == '__main__':
	filepath = getFile()
	print("Destination  = {}".format(destDIR))

	if os.path.isdir(filepath):
		destDIR = filepath
		transcribeDIR(filepath)
	else:
		destDIR = os.path.dirname(filepath)
		transcribeFile(filepath, destDIR)

