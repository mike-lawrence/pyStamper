class stamperClass:
	def start(self,windowSize,windowPosition):
		import billiard
		billiard.forking_enable(0)
		self.qTo = billiard.Queue()
		self.qFrom = billiard.Queue()
		self.process = billiard.Process( target=stamperLoop , args=(windowSize,windowPosition,self.qTo,self.qFrom,) )
		self.process.start()
		return None
	def end(self):
		self.qTo.put(['quit'])
		self.process.terminate()
		del self.qTo
		del self.qFrom
		return None


def stamperLoop(windowSize,windowPosition,qTo,qFrom):
	import sdl2
	import sdl2.ext
	import sys
	try:
		import appnope
		appnope.nope()
	except:
		pass
	sdl2.SDL_Init(sdl2.SDL_INIT_TIMER)
	timeFreq = 1.0/sdl2.SDL_GetPerformanceFrequency()
	sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
	window = sdl2.ext.Window("Timestamper", size= windowSize,position=windowPosition,flags=sdl2.SDL_WINDOW_SHOWN)
	window.refresh()
	sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
	gamepad = sdl2.SDL_JoystickOpen(0)
	while True:
		sdl2.SDL_PumpEvents()
		if not qTo.empty():
			message = qTo.get()
			if message[0]=='quit':
				sys.exit()
		for event in sdl2.ext.get_events():
			message = {}
			if event.type==sdl2.SDL_KEYDOWN:
				message['type'] = 'key'
				message['time'] = event.key.timestamp*timeFreq
				message['value'] = sdl2.SDL_GetKeyName(event.key.keysym.sym).lower()
				qFrom.put(message)
			elif event.type == sdl2.SDL_JOYAXISMOTION:
				message['type'] = 'axis'
				message['axis'] = event.jaxis.axis
				message['time'] = event.jaxis.timestamp*timeFreq
				message['value'] = event.jaxis.value
				qFrom.put(message)

