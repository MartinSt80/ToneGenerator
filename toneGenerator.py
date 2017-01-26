from tkinter import *
from tkinter import ttk
import pygame, math
import numpy as np

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=8192)
root = Tk()

def SineObject(*args):
	frames = np.linspace(0, 2 * math.pi, 44100)
	values = []
	for n in frames:
		if len(args) == 1:
			values.append(int(32767 * (math.sin(args[0] * n))))
		else:
			values.append(int(32767 * (0.5 * math.sin(args[1] * n) + 0.5 * math.sin(args[0] * n))))
	return pygame.sndarray.make_sound(np.array(values))

def checkChannel():
	if CHANNEL1_IS_ACTIVE.get() or CHANNEL2_IS_ACTIVE.get():
		startSound()
	else:
		snd.stop()

def startpressed():
	global START_IS_PRESSED
	START_IS_PRESSED = True
	checkChannel()

def stoppressed():
	global START_IS_PRESSED
	START_IS_PRESSED = False
	pygame.mixer.stop()

def startSound(*args):
	if START_IS_PRESSED:
		if CHANNEL1_IS_ACTIVE.get() and CHANNEL2_IS_ACTIVE.get():
			snd.play(SineObject(CHANNEL1_SETFREQ.get(), CHANNEL2_SETFREQ.get()), loops=-1)
		elif CHANNEL1_IS_ACTIVE.get():
			snd.play(SineObject(CHANNEL1_SETFREQ.get()), loops=-1)
		elif CHANNEL2_IS_ACTIVE.get():
			snd.play(SineObject(CHANNEL2_SETFREQ.get()), loops=-1)

def state_of_play():
	if not CHANNEL1_IS_ACTIVE.get() and not CHANNEL2_IS_ACTIVE.get():
		play_button.state(["disabled"])
	else:
		play_button.state(["!disabled"])

snd = pygame.mixer.Channel(1)

CHANNEL1_SETFREQ = IntVar()
CHANNEL1_SETFREQ.set(400)
CHANNEL2_SETFREQ = IntVar()
CHANNEL2_SETFREQ.set(200)

START_IS_PRESSED = False
STOP_IS_PRESSED = False

CHANNEL1_IS_ACTIVE = BooleanVar()
CHANNEL1_IS_ACTIVE.set(False)
CHANNEL2_IS_ACTIVE = BooleanVar()
CHANNEL2_IS_ACTIVE.set(False)

root.title("Tone Generator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

channel1_frame = ttk.Frame(mainframe, padding="3 3 12 12")
channel1_frame.grid(column=0, row=0)
channel1_activebox = ttk.Checkbutton(channel1_frame, text='Channel 1 Active', variable=CHANNEL1_IS_ACTIVE, command=checkChannel)
channel1_activebox.grid(column=0, row=0, sticky=W)
channel1_display = ttk.Entry(channel1_frame, text=CHANNEL1_SETFREQ, textvariable=CHANNEL1_SETFREQ, width=4)
channel1_display.bind('<Return>', startSound)
channel1_display.grid(column=1, row=0,sticky=E)
ttk.Label(channel1_frame, text='Hz').grid(column=2, row=0, sticky=W)
channel1_freqslider = ttk.Scale(channel1_frame, from_=200, to=6000, length=300, value=CHANNEL1_SETFREQ.get(), variable=CHANNEL1_SETFREQ, command=startSound)
channel1_freqslider.grid(column=0, row=1, columnspan=3)

channel2_frame = ttk.Frame(mainframe, padding="3 3 12 12")
channel2_frame.grid(column=0, row=1)
channel2_activebox = ttk.Checkbutton(channel2_frame, text='Channel 2 Active', variable=CHANNEL2_IS_ACTIVE, command=checkChannel)
channel2_activebox.grid(column=0, row=0, sticky=W)
channel2_display = ttk.Entry(channel2_frame, text=CHANNEL2_SETFREQ, textvariable=CHANNEL2_SETFREQ, width=4)
channel2_display.bind('<Return>', startSound)
channel2_display.grid(column=1, row=0,sticky=E)
ttk.Label(channel2_frame, text='Hz').grid(column=2, row=0, sticky=W)
channel2_freqslider = ttk.Scale(channel2_frame, from_=200, to=6000, length=300, value=CHANNEL2_SETFREQ.get(), variable=CHANNEL2_SETFREQ, command=startSound)
channel2_freqslider.grid(column=0, row=1, columnspan=3)

play_button = ttk.Button(mainframe, text="Start", command=startpressed).grid(column=1, row=3)
stop_button = ttk.Button(mainframe, text="Stop", command=stoppressed).grid(column=2, row=3)
quit_button = ttk.Button(mainframe, text="Quit", command=root.destroy).grid(column=3, row=3)

root.mainloop()



#if START_IS_PRESSED and CHANNEL1_IS_ACTIVE.get():
