import math
from tkinter import *
from tkinter import ttk
import pygame
import numpy as np


class ToneGenerator:

	def __init__(self):
		pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=8192)

		self.channel1_mixer = pygame.mixer.Channel(1)
		self.channel2_mixer = pygame.mixer.Channel(2)

		self.root = Tk()
		self.root.title("Tone Generator")

		self.channel1_freq = StringVar()
		self.channel1_freq.set(400)
		self.channel2_freq = StringVar()
		self.channel2_freq.set(200)

		self.sound_started = False

		self.channel1_active = BooleanVar()
		self.channel1_active.set(False)
		self.channel2_active = BooleanVar()
		self.channel2_active.set(False)

		self.mainframe = self.__draw_mainframe()

		self.channel1_frame = self.__draw_channelframe(self.channel1_active, self.channel1_freq)
		self.channel1_frame.grid(column=0, row=0)
		self.channel2_frame = self.__draw_channelframe(self.channel2_active, self.channel2_freq)
		self.channel2_frame.grid(column=0, row=1)

		self.play_button = self.__draw_buttonframe()

		self.root.mainloop()

	def __draw_mainframe(self):
		mainframe = ttk.Frame(self.root, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		mainframe.columnconfigure(0, weight=1)
		mainframe.rowconfigure(0, weight=1)
		return mainframe

	def __draw_channelframe(self, channel_active, channel_freq):
		channel_frame = ttk.Frame(self.mainframe, padding="3 3 12 12")

		channel_activebox = ttk.Checkbutton(channel_frame,
											text='Activate Channel',
											variable=channel_active,
											command=self.__start_sound)
		channel_activebox.grid(column=0, row=0, sticky=W)

		channel1_display = ttk.Entry(channel_frame,
									 text=channel_freq,
									 textvariable=channel_freq,
									 width=4)
		channel1_display.bind('<Return>', self.__start_sound)
		channel1_display.grid(column=1, row=0, sticky=E)

		ttk.Label(channel_frame, text='Hz').grid(column=2, row=0, sticky=W)

		channel_freqslider = ttk.Scale(channel_frame,
									   from_=200,
									   to=2000,
									   length=300,
									   value=channel_freq.get(),
									   variable=channel_freq,
									   command=self.__start_sound)
		channel_freqslider.grid(column=0, row=1, columnspan=3)

		return channel_frame

	def __draw_buttonframe(self):
		button_frame = ttk.Frame(self.mainframe, padding="3 3 12 12")
		button_frame.grid(column=0, row=2)
		play_button = ttk.Button(button_frame, text="Start", command=self.__start_pressed)
		play_button.grid(column=0, row=0)
		quit_button = ttk.Button(button_frame, text="Quit", command=self.root.destroy).grid(column=1, row=0)
		return play_button

	def __start_sound(self, event=None):
		self.channel1_freq.set(self.channel1_freq.get().split('.')[0])
		self.channel2_freq.set(self.channel2_freq.get().split('.')[0])
		if self.sound_started:
			if self.channel1_active.get():
				self.channel1_mixer.play(self.__calc_sine_sound(int(self.channel1_freq.get())), loops=-1)
			else:
				self.channel1_mixer.stop()

			if self.channel2_active.get():
				self.channel2_mixer.play(self.__calc_sine_sound(int(self.channel2_freq.get())), loops=-1)
			else:
				self.channel2_mixer.stop()

	def __start_pressed(self):
		if self.play_button['text'] == 'Start':
			self.sound_started = True
			self.__start_sound()
			self.play_button['text'] = 'Stop'

		else:
			self.sound_started = False
			pygame.mixer.stop()
			self.play_button['text'] = 'Start'

	def __calc_sine_sound(self, freq):
		calc_sine = lambda x: int(32767 * (math.sin(freq * x)))
		frames = np.linspace(0, 2 * math.pi, 44100)
		values = np.array([calc_sine(x) for x in frames])
		return pygame.mixer.Sound(values)


ToneGenerator()

