# clockApp.py

__all__ = [ 'The_Clock_App' ]

from	threading	import	RLock	# Re-entrant mutex lock, used for thread-safety in Clock app.
from	time		import	sleep	# Causes thread to give up control for a period. Used in ClockThread.

from	infrastructure.logmaster	import getLoggerInfo, ThreadActor

global _logger		# Logger serving the current module.
global _component	# Name of our software component, as <sysName>.<pkgName>.
			
(_logger, _component) = getLoggerInfo(__file__)		# Fill in these globals.

from	infrastructure.decorators	import	singleton
		# A simple decorator for singleton classes.

from	infrastructure.time		import	envTZ, timeZone, tznow, tzAbbr
		# Time-zone related functions we use in the Clock app.

from	.application			import	Application_
		# Base class from which we derive subclasses for specific applications.

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Clock_App_(Application_):	pass

class ClockThread: pass

class ClockThread(ThreadActor):

	"""A simple thread to operate the clock. This just calls
		the clock app's .doTick() method once per second."""

	defaultRole = 'Clock'	# This will appear in our log lines.
	
		#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		#| Set this class variable to fill in the 'component' parameter
		#| automatically for all log records generated by this thread. 				

	defaultComponent = _component
			# Use value obtained earlier from getLoggerInfo().
			
	def __init__(newClockThread:ClockThread, clockApp:Clock_App_):

		_logger.debug("[Clock Apps] Creating thread to drive clock updates.")

		thread = newClockThread
		thread.app = clockApp		# Remember pointer to app.

		thread.exitRequested = False

		thread.defaultTarget = thread._main
		super(ClockThread, thread).__init__(daemon=True)

	def _main(thisClockThread:ClockThread):

		"""Main routine of clock thread. Pretty straightforward."""

		thread = thisClockThread
		app = thread.app

		wakeupInterval = 1	# How many seconds between time checks.
			# Since this is 1 second, our clock display will be accurate
			# to within a second.

		while not thread.exitRequested:

			sleep(wakeupInterval)	# Sleep until next wakeup.

				# All we do is send a 'tick' event to the Clock app,
				# and it does all the real work.
			app.doTick()

@singleton
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class The_Clock_App(Clock_App_):

	"""The 'Clock' app displays the current date and time.
		Right now, its only optional parameter setting is
		its 'mode', which can be either 'minutes' or
		'seconds', to control whether seconds are displayed."""

		# Default format string to use in 'minutes' mode.
	_DEFAULT_MINUTES_FORMAT = "%A, %B %d, %Y, %I:%M %p"
			# This is like: Sunday, January 17, 2021, 12:02 PM MST

		# Default format string to use in 'seconds' mode.
	_DEFAULT_SECONDS_FORMAT = "%A, %B %d, %Y, %I:%M:%S %p"
			# This is like: Sunday, January 17, 2021, 12:02:42 PM MST

	def appSpecificInit(thisClockApp:Clock_App_, conf:dict):

		"""This method performs application-specific initialization
			for the Clock application, at app creation time."""

		app = thisClockApp
		win = app.window		# Gets our window (already created).

		app._lock = RLock()		# Reentrant mutex lock.

		app._lastTime = None	# No time readings yet.
		app._timeStr = None

			# Get the time zome preference from the system config.
		tz = timeZone()

			# We store the time zone object for later reference.
		app._timezone = tz

			# Get the mode config.
		if 'mode' in conf:
		 	mode = conf['mode']		# 'minutes' or 'seconds'
		else:
			mode = 'minutes'	# Default to 'minutes.'

		app._mode = mode

			# Tell our window to please word-wrap and auto-size itself.
		win.wordWrap = True		# However, time shouldn't overflow anyway.
		win.autoSize = True

			# Do one 'tick' initially at init time.
			# Further ticks will be invoked by the clock thread (below).
		app.doTick()

			# Create and start up the clock thread.
		app._thread = thread = ClockThread(app)
		thread.start()
				# This starts the clock running in the background.

	def doTick(thisClockApp):

		"""This method is called when the clock ticks (which happens
			once per second).  It updates the display if needed.
			The time is accurate to the system clock within 1 second."""

		app = thisClockApp

			# Go ahead and make a note of the current time.
		app.updateTime()

			# Go ahead and regenerate our time string.
		app.updateTimeStr()
				# This also updates the display if needed.

	def updateTime(thisClockApp):

		app = thisClockApp

		with app._lock:
			app._lastTime = tznow()		# Updates our time record w. current time.


	def updateTimeStr(thisClockApp):

		app = thisClockApp

		timeChanged = False

		# Do the following atomically to maintain consistency
		# of data structures.

		with app._lock:

				# Retrieve the last saved time string.
			oldTimeStr = app._timeStr

				# Get the current time string.
			newTimeStr = app.timeString()

				# Are they different? Then time has changed.
			if newTimeStr != oldTimeStr:

				# Save the new time string.
				app._timeStr = newTimeStr

				timeChanged = True

		# Did the time change? Then we need to update
		# our window's underlying text buffer.
		if timeChanged:

			win = app.window

			# If the window already has some text, clear it first.
			if win.nTextRows > 0:
				win.clearText()		# Doesn't update image/display yet.

			# Now we add the new text.
			win.addText("The time is:  " + newTimeStr)
				# Note this does update the image, field view & display.
				# However, it does not notify the AI if our config
				# record has quiet-update = true.


	def timeString(thisClockApp):

		"""Returns the time string for the last saved time."""

		app = thisClockApp
		mode = app._mode

		if mode == 'minutes':
			fmtstr = app._DEFAULT_MINUTES_FORMAT
		else:
			fmtstr = app._DEFAULT_SECONDS_FORMAT

		# Is the 'TZ' environment variable set?
		# If so, then we can add '(%Z)' (time zone abbreviation) to the format str.
		if envTZ is not None:
			fmtstr = fmtstr + " (%Z)"

		with app._lock:
			lastTime = app._lastTime
			timeStr = lastTime.strftime(fmtstr)

		# If 'TZ' was not set, then we have to try to guess the time zone name from the offset.
		if envTZ is None:
			tzAbb = tzAbbr()
			timeStr = timeStr + f" ({tzAbb})"

		return timeStr

