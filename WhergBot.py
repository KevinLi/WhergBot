#!/usr/bin/python2

import Core
from threading import Timer

nick = 'WhergBot'
real = 'WhergBot [Ferus]'
ident = 'Wherg'
channels = ['#hacking', '#lobby' ,'#4chon' ,'#circlejerk' ,'#tinyboard' ,'#animu', '#games']
#channels = ['#h']
owner = ['Ferus', 'anonymous@the.interwebs', 0]
ssl = True
if ssl:
	port = 6697
else:
	port = 6667

if __name__ == '__main__':
	try:
		WhergBot = Core.Bot(nick, real, ident, owner, ssl)
		WhergBot.Connect(server='opsimathia.datnode.net', port=port)
		if WhergBot.Nickserv.password != '':
			_p = Timer(3, WhergBot.Identify, ())
			_p.daemon = True
			_p.start()
		_t = Timer(5, WhergBot.irc.join, (",".join(channels),))
		_t.daemon = True
		_t.start() 

		while WhergBot.irc._isConnected:
			WhergBot.Parse(WhergBot.irc.recv(bufferlen=1024))
		else:
			WhergBot.irc.close()
			quit()
			
	except KeyboardInterrupt:
		print("\n* [Core] Interrupt Caught; Quitting!")
		WhergBot.p.command.Quit("KeyboardInterrupt Caught!")
