#!/usr/bin/env python
from .Settings import Settings

class Main(object):
	def __init__(self, Name, Parser):
		self.__name__ = Name
		self.Parser = Parser
		self.IRC = self.Parser.IRC
	
	def Exec(self, data):
		if data[0] not in Settings['Allowed']:
			self.IRC.notice(data[0].split('!')[0], "You lack the required authority to use this command.")
			return None
		try:
			exec(" ".join(data[3:]).replace(":@exec ", ""))
		except SyntaxError, e:
			self.IRC.say(data[2], repr(e))

	def Load(self):
		self.Parser.hookCommand('PRIVMSG', Settings.get("Regex"), self.Exec)
		self.Parser.loadedPlugins[self.__name__].append(Settings)
		self.Parser.loadedPlugins[self.__name__].append(self.Load)
		self.Parser.loadedPlugins[self.__name__].append(self.Unload)
		self.Parser.loadedPlugins[self.__name__].append(self.Reload)
	def Unload(self):
		del self.Parser.loadedPlugins[self.__name__]
	def Reload(self):
		pass
