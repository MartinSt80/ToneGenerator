from tkinter import *
from tkinter import ttk
import pygame, math
import numpy as np


pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=8192)

def SineObject(freq):
	frames = np.linspace(0, 2 * math.pi, 44100)
	values = []
	for n in frames:
		values.append(int(32767 * math.sin(freq * n)))
	return pygame.sndarray.make_sound(np.array(values))

CHANNEL1_SETFREQ = 400
CHANNEL1_ACTIVE = False
START_IS_PRESSED = False

def setChannel1(freq1):
	global CHANNEL1_SETFREQ
	CHANNEL1_SETFREQ = int(float(freq1))
	startSound()

def startpressed():
	global START_IS_PRESSED
	START_IS_PRESSED = True
	startSound()

def stoppressed():
	global START_IS_PRESSED
	START_IS_PRESSED = False
	pygame.mixer.stop()

def startSound():

	if START_IS_PRESSED:
		snd1.play(SineObject(CHANNEL1_SETFREQ), loops=-1)
	# snd2.play(SineObject(500 + 2), loops=-1)

snd1 = pygame.mixer.Channel(1)
snd2 = pygame.mixer.Channel(2)

root = Tk()
root.title("Tone Generator")


channel1_is_active = BooleanVar()
channel2_is_active = BooleanVar()
channel1_is_active = False
channel2_is_active = False
channel1_freq = StringVar()
channel1_freq = CHANNEL1_SETFREQ

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

channel1_frame = ttk.Frame(mainframe, padding="3 3 12 12")
channel1_frame.grid(column=1, row=1, columnspan=3, sticky=(W))
channel1_activebox = ttk.Checkbutton(channel1_frame, text='Channel 1 Active', variable=channel1_is_active)
channel1_activebox.grid(column=1, row=1, sticky=(W))
channel1_freqslider = ttk.Scale(channel1_frame, from_=200, to=6000, length=300, value=CHANNEL1_SETFREQ, variable=channel1_freq, command=setChannel1)
channel1_freqslider.grid(column=1, row=2, columnspan=2, sticky=(W))
#channel1_freqdisplay = ttk.text(channel1_frame, textvariable=int(channel1_freq))
#channel1_freqdisplay.grid(column=2, row=1, sticky=(E))

channel2_frame = ttk.Frame(mainframe, padding="3 3 12 12")
channel2_frame.grid(column=1, row=2, columnspan=3, sticky=(W))

play_button = ttk.Button(mainframe, text="Start", command=startpressed)
stop_button = ttk.Button(mainframe, text="Stop", command=stoppressed)
quit_button = ttk.Button(mainframe, text="Quit", command=root.destroy)
play_button.grid(column=1, row=3)
stop_button.grid(column=2, row=3)
quit_button.grid(column=3, row=3)

root.mainloop()





