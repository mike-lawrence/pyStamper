class stamperClass:
	def start(self,windowSize=(200,10),windowPosition=(0,0),windowColor=(255,255,255),doBorder=True):
		import billiard
		billiard.forking_enable(0)
		self.qTo = billiard.Queue()
		self.qFrom = billiard.Queue()
		self.process = billiard.Process( target=stamperLoop , args=(windowSize,windowPosition,windowColor,doBorder,self.qTo,self.qFrom,) )
		self.process.start()
		return None
	def quit(self):
		self.qTo.put(['quit'])
		self.process.join()
		del self.qTo
		del self.qFrom
		return None


def stamperLoop(windowSize,windowPosition,windowColor,doBorder,qTo,qFrom):
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
	if doBorder:
		flags = sdl2.SDL_WINDOW_SHOWN
	else:
		flags = sdl2.SDL_WINDOW_BORDERLESS | sdl2.SDL_WINDOW_SHOWN
	window = sdl2.ext.Window("pyStamper",size=windowSize,position=windowPosition,flags=flags)
	windowSurf = sdl2.SDL_GetWindowSurface(window.window)
	sdl2.ext.fill(windowSurf.contents,sdl2.pixels.SDL_Color(r=windowColor[0], g=windowColor[1], b=windowColor[2], a=255))
	window.refresh()
	#sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) #uncomment if you want joystick input
	#sdl2.SDL_JoystickOpen(0) #uncomment if you want joystick input
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

