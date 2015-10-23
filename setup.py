import Tkinter
import json
from riotwatcher import RiotWatcher
import riotwatcher as rw
class SetupApp(Tkinter.Tk):
	def __init__(self, parent):
		Tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.load_settings()
		self.initialize()

	def initialize(self):
		self.grid()

		# Text fields
		self.summoner = Tkinter.Entry(self)
		self.summoner.grid(column=1, row=1, sticky='ew')

		self.apikey = Tkinter.Entry(self)
		self.apikey.grid(column=1, row=0, sticky='ew')

		self.region_var = Tkinter.StringVar(self)
		self.region_var.set("na")
		try:
			self.apikey.insert(0, self.settings['apikey'])
			self.summoner.insert(0, self.settings['summonerName'])
			self.region_var.set(self.settings['region'])
		except:
			pass
		
		#regions dropdown menu
		self.region = Tkinter.OptionMenu(self, self.region_var, rw.BRAZIL, rw.EUROPE_NORDIC_EAST, rw.EUROPE_WEST, rw.KOREA, rw.LATIN_AMERICA_NORTH, rw.LATIN_AMERICA_SOUTH, rw.NORTH_AMERICA, rw.OCEANIA, rw.RUSSIA, rw.TURKEY)
		self.region.grid(column=1, row=2)

		# submit button
		button = Tkinter.Button(self, text=u'save', command=self.on_button_click)
		button.grid(column=1, row=3)

		# labels
		label = Tkinter.Label(self, text='Summoner Name:')
		label.grid(column=0, row=1,columnspan=1, sticky='ew')

		label2 = Tkinter.Label(self, text='API Key:')
		label2.grid(column=0, row=0,columnspan=1, sticky='ew')

		label3 = Tkinter.Label(self, text='Region:')
		label3.grid(column=0, row=2, columnspan=1, sticky='ew')

		# error label
		self.error_label = Tkinter.Label(self, text='')
		self.error_label.grid(column=0, row=4, columnspan=2, sticky='ew')

	def load_settings(self):
		try:
			with open("settings.json") as f:
				self.settings = json.load(f)
		except:
			print 'error'
			self.error_label.configure(text='Could not load settings!')
			self.settings = {}


	def on_button_click(self):
		self.error_label.configure(text='validating...')

		w = RiotWatcher(self.apikey.get())
		#validate summoner name and api key
		try:
			me = w.get_summoner(name=self.summoner.get(), region=self.region_var.get())
			print me
			#save new settings
			self.settings['summonerName'] = self.summoner.get()
			self.settings['region'] = self.region_var.get()
			self.settings['apikey'] = self.apikey.get()
			with open('settings.json', 'w') as f:
				json.dump(self.settings, f)
			self.error_label.configure(text='settings saved!')

		except Exception as error:
			if error.error == "Unauthorized":
				self.error_label.configure(text='API Key is invalid!')
			else:
				self.error_label.configure(text='Summoner does not exist!')

	def on_press_enter(self,event):
		self.on_button_click()

if __name__=="__main__":
	app = SetupApp(None)
	app.title("LoLBuilds Setup")
	app.mainloop()

