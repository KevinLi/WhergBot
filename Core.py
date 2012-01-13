#Global Imports
from blackbox import blackbox
from time import sleep

#Local Imports
import Parser
from Services import NickServ, HostServ, Allowed

class Bot():
	def __init__(self, nickname='', realname='', ident='', owner=[], ssl=True, proxy=None):
		'''Create our bots name, realname, and ident, and create our IRC object, Commands object, Parser object, and users dict'''
		self.irc = blackbox.IRC(logging=False, ssl=ssl)
		if proxy:
			try:
				print("* [IRC] Attempting to set proxy to {0} on port {1}".format(proxy[0][0], proxy[0][1]))
				import socks
				Proxy = proxy[0]
				Types = {"http":socks.PROXY_TYPE_HTTP, "socks4":socks.PROXY_TYPE_SOCKS4, "socks5":socks.PROXY_TYPE_SOCKS5}
				Sock = socks.socksocket()
				Sock.setproxy(Types[proxy[1]], Proxy[0], int(Proxy[1]))
				self.irc._irc = Sock
				print("* [IRC] Set proxy, if the bot fails to connect, the proxy may be bad.\n* [IRC] This does not set a proxy for any HTTP GET/POST/etc requests.")
			except Exception, e:
				print("* [IRC] Failed to set proxy, using none.")
				print(repr(e))

		self.Nickserv = NickServ.NickServ(sock=self.irc)
		self.Hostserv = HostServ.HostServ(sock=self.irc)
		
		self.allowed = Allowed.Allowed("Services/AllowedUsers.shelve")
		
		if owner:
			self.Owner = owner
			self.allowed.Owner = self.Owner
			self.allowed.db[self.Owner[0]] = [self.Owner[1], self.Owner[2]] #Reset the owner. Just in case the config changed.
			print("* [Access] Setting owner to {0}, with hostmask {1}".format(self.Owner[0], self.Owner[1]))
		
		self.p = Parser.Parse(sock=self.irc, allowed=self.allowed, nick=nickname)
				
		if nickname:
			self.nickname = nickname
		else:
			self.nickname = 'WhergBot2'
		if realname:
			self.realname = realname
		else:
			self.realname = 'WhergBot [Ferus]'
		if ident:
			self.ident = ident
		else:
			self.ident = 'Wherg'

		
	def Connect(self, server, port=6697):
		'''Connect to the server, default the port to 6697 because SSL'''
		self.irc.connect(server, port)
		print("* [IRC] Connecting to {0} on port {1}".format(server, port))
		self.irc.username(self.ident, self.realname)
		print("* [IRC] Sending username: {0} and realname: {1}".format(self.ident, self.realname))
		self.irc.nickname(self.nickname)
		print("* [IRC] Sending nickname: {0}".format(self.nickname))
		try:
			#Unreal has a fucking bug where you have to wait until you
			#recieve a line after registering to continue.
			while True:
				if self.irc.recv(1):
					break
		except:
			quit()
		self.irc.send("MODE {0} +Bs".format(self.nickname))
		
	def Identify(self):
		self.Nickserv.Identify()
		sleep(.3)
		
	def Parse(self, msg):
		try:
			if not msg:
				self.irc._isConnected = False
				self.irc.close()
				raise blackbox.blackbox_core.IRCError('Pinged out?')
			else:
				self.msg = self.p.Main(msg)
		except blackbox.blackbox_core.IRCError, e:
			import sys
			sys.exit("* [IRC] Error: {0}".format(e))
		except Exception, e:
			print("* [Error] {0}, {1}".format(repr(e), e.__class__))
			#self.irc.close()
			#quit()
