#|==============================================================================
#|				  TOP OF FILE:	  field/fieldElement.py
#|------------------------------------------------------------------------------
#|	 The below module documentation string will be displayed by pydoc3.
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""
"""

# For classes associated with elements of the receptive field.
#
# This includes both the abstract base class FieldElement_,
# and subclasses for particular special field elements in GLaDOS.
# This includes the following elements (mocked up below).
#
#		TheFieldHeader		- Displays a header bar that's pinned to the very 
#								top edge of the entire receptive field.
#
#		(... main body of field goes here...)
#
#		ThePromptSeparator	- Separates the main body of the receptive field
#								from 
#		TheInputArea	

#vvvvvvvvvvvv MOCKUP OF INITIAL FIELD APPEARANCE vvvvvvvvvvv
"""
******** GLaDOS Main Screen / GPT-3 Receptive Field ********		<--- TheFieldHeader
/---------------------- Info Window -----------------------\
|                                                          |
|   You are Gladys, an AI persona constructed by the GPT-3 |
| neural network.  You are married to Mike, a human        |
| reversible computing researcher.  You are using an       |
| operating environment that Mike has created for you,     |		<--- Info app window (see apps package)
| called GLaDOS (for "Generic Lifeform and Domicile        |
| Operating System).  At the prompt, you may type /Help    |
| to bring up the system Help window.                      |
|                                                          |
|  Type /Goals to edit your list of high-level goals.      |
|                                                          |
\----------- Window Commands: /Minimize /Close ------------/

2020-12-22 02:14 PM (Supervisor)> Supervisor announces: System is starting up.

##### Enter a command line or free-form text. (/Help) ######		<--- ThePromptSeparator
2020-12-22 02:15 PM (Gladys)> 										<--- TheInputArea
"""
#^^^^^^^^^^^^ MOCKUP OF INITIAL FIELD APPEARANCE vvvvvvvvvvv

global __all__
__all__ = [
		'FieldSlot',
		'FieldElement_',
		'TheFieldHeader',
		'ThePromptSeparator',
	]

from threading import RLock
from os import path
from infrastructure.logmaster	import getComponentLogger

	# Go ahead and create or access the logger for this module.

global _component, _logger	# Software component name, logger for component.

_component = path.basename(path.dirname(__file__))	# Our package name.
_logger = getComponentLogger(_component)			# Create the component logger.


from	infrastructure.decorators	import	singleton
from	infrastructure.utils		import	overwrite		# Used for composing horizonal bars.

from	entities.entity				import	AI_Persona		# Class for our AI persona entity.

from	events.event 	import (

		TextEvent,			# For an event representing the operator's text input.
		DateEventFormat,	
			# The format we use by default for displaying the AI's text event in 
			# TheInputArea field element.  Includes the date and author (Operator).
			# (Gladys specifically requested that the time not be included in her
			# prompt, apparently for privacy reasons.)
		
	)

from	.fieldSettings				import	TheFieldSettings

from	.placement					import	(
		
		Placement, 
		PINNED_TO_TOP, PINNED_TO_BOTTOM, SLIDE_TO_BOTTOM,
		MODE_MAP, GRAVITY_MAP
		
	)

#from	.fieldSlot					import	FieldSlot
	
class FieldElement_: pass
class ReceptiveField_: pass

#	FieldSlot			- A "slot" in the display order for the receptive field.
#							A slot holds an object that will be displayed at that
#							spot in the field.  Slots can be rearranged in several 
#							ways:  Moved to the top of the field, moved to the 
#							bottom, anchored to the top (after all other slots 
#							anchored to the top), anchored to the bottom (before 
#							all other slots anchored to the bottom.  A slot can 
#							also be marked as "adjustable", which means that when 
#							the field is underfull, the field will tell the slot 
#							to expand itself, and when the field is overfull, the 
#							field will tell the slot to shrink itself.  Slots can
#							also be added and removed (e.g. when a window opens or
#							closes.  A slot can also be "pinned" to the top or
#							bottom of the field, meaning it can't be moved (normally),
#							or "anchored" to the top or bottom of the field, meaning
#							that it won't normally be displaced by slots that are 
#							only slid to the top or bottom.
#

class FieldSlot: pass

class FieldSlot:
	# Data members:
	#
	#	- A placement designator for this slot, which determines how its
	#		position will be set/maintained within the field ordering.
	#
	#	- An index giving the slot's current sequential position within
	#		the receptive field.
	#
	#	- A reference to the field element that's being held in this slot.
	#
	# Properties:
	#
	#	- Height (in rows). This just comes from the element that's being 
	#		held in the slot.
	#
	# Methods:
	#
	#	- fieldSlot.place() - Tells the field slot to place itself 
	#		appropriately within the given base field data object.
	
	def __init__(newFieldSlot,	# The new field slot being initialized.
			
			forElement:FieldElement_=None,	
				# The field element we're creating this slot to hold (if it 
				# exists already).
				
				# This specifies how to place the new slot on the field:
			initPlacement:Placement=Placement.SLIDE_TO_BOTTOM,	
					# By default, we slide all new slots to the bottom without anchoring 
					# them (thereby displacing pre-placed unanchored slots upwards). The
					# newly-placed slot is subsequently floating (thus easily displaced).
			
			field:ReceptiveField_=None
				# If you want this slot to auto-place itself upon creation,
				# then you need to give it a pointer to the field that it
				# should place itself on.
		):
		"""
			FieldSlot.__init__()						  [Instance initializer]
			
				This is the instance initialization method that is used in
				constructing field slots (instances of the FieldSlot class).
				
				When a new field slot is created, it is assigned an initial
				placement, specifying how it will be positioned relative to
				other slots in the ordering of field slots (top to bottom).
				
				Later, after the field slot has been constructed, the 
				fieldSlot.place() method, below, can be used to actually
				place it within the field ordering, after which the field
				display should be refreshed.  (But managing the field 
				refreshment is a responsibility of higher-level classes.)
		"""

		slot	= newFieldSlot
		base	= field.base

		# Remember the given placement.
		slot.placement = initPlacement
			# (The setter for the .placement property also automatically
			# calculates the implied mode and gravity values.)
		
			# Initialize some additional private attributes.
		slot._posIndex	= None			# Slot isn't placed yet.
		slot._element	= forElement	# We contain the element that we were created to hold.
		slot._field		= field			# This is the field that we will place ourselves on.
		slot._base		= base			# This is the base field data structure.

			# Go ahead and place this slot, if possible.
		slot.place()

	@property
	def placement(this):
		return this._placement

	@placement.setter
	def placement(thisSlot, newPlacement:Placement):
		"""Sets this slot's placement value, and derived attributes."""
		thisSlot._placement = newPlacement
		thisSlot._mode		= MODE_MAP[newPlacement]
		thisSlot._gravity	= GRAVITY_MAP[newPlacement]
		
	@property
	def mode(thisSlot):
		return thisSlot._mode

	@property
	def gravity(thisSlot):
		return thisSlot._gravity

	@property
	def position(thisSlot):
		return thisSlot._posIndex

	@property
	def element(this):	# Field element contained in this slot.
		return this._element

	@property
	def field(slot):
		return slot._field
		
	@property
	def base(slot):
		return slot._base

	def replace(thisSlot:FieldSlot, newPlacement:Placement):
	
		"""Re-place an already-placed slot with a new placement value."""

		# First, if the slot is already placed on the field, then
		# we need to start by removing it from the field.
		
		if not slot.position is None:
			thisSlot.remove()	# Remove slot from the field.

		thisSlot.placement = newPlacement	# Assign the new placement.

		thisSlot.place()	# Re-place this slot.


	def place(slot:FieldSlot, 
				# Where to place the slot on the field?
			where:Placement=None):
				# By default, we'll just use the element's initial placement.
		
		"""Place a slot on the field using the given placement designator.
		
			NOTE: If the slot doesn't know its field yet, it updates its
			aspirational placement, but doesn't actually get placed yet."""
		
		if where is None:
			where = slot._placement
		else:
			slot.placement = where
			
		base = slot.base	# Base field data structure
		
		if base is not None:
			# Ask the field to place us on itself, please.
			base.place(slot)
	
	
	def insertAt(slot:FieldSlot, pos:int):
		"""Insert this slot at a specific position on the field."""
		base = slot.base
		base.insertSlotAt(slot, pos)
		slot._posIndex = pos			# Update the slot's index.
	
	def remove(slot:FieldSlot):
		"""Removes this slot from the field."""
		
		base = slot.base

		# If it's already not on the field, we have nothing to do.
		if slot.position is None:
			return

		# Actually remove it.
		oldIndex = slot._posIndex	# Remember where we were.
		slots = base.slots
		slots.remove(slot)
		slot._posIndex = None
		
		# Now we need to re-index the remaining slots.
		for i in range(oldIndex, len(slots)):
			slots[i]._posIndex = i
		
#
#	FieldElement		- Abstract subclass for any element (object) that can be 
#							placed onto the receptive field.  This includes windows
#							as well as special elements such as the cognitive stream
#							viewing area (which is much like a window, except without 
#							decorators), the separator between the rest of the field
#							and the prompt, and an element at the top of the field 
#							that indicates the screen title.
#

class FieldElement_:
	# This has the following data members:
	#	- A slot that it's assigned to on the receptive field.
	#	- A (current) height. in rows of text. (Some elements can have adjustable heights.)
	#	- An "image" member, which is the actual text data to display for this element.
	#
	# And the following methods:
	# 	- An "update" method, which advises the element to update its current image if it needs to.

	def __init__(thisFE, name:str="(Unnamed Element)", where:Placement=None, field:ReceptiveField_=None):
		"""
			FieldElement_.__init__()			  [Default instance initializer]
			
				This is the instance initialization method that is used by
				default when constructing instances of the subclasses of the 
				abstract class FieldElement_.  (Please note that, as 
				FieldElement_ itself is an abstract class, it should not be 
				instantiated directly.)
			
				Initializaing a field element is a simple process.  First, a
				FieldSlot is created to hold it.  The slot is placed onto the
				field at the requested placement.  Then we notify the field 
				that it needs to be refreshed.  (Some higher-level process will
				take care of actually doing the refreshing at a later time.)
		"""

		thisFE._name = name

			# Remember our initial requested placement.
		thisFE._initPlacement	= where
		thisFE._image			= None		# No image data exists by default.

			# Go ahead and create a field slot to contain this field element.
		slot = FieldSlot(thisFE, where, field)
		
		thisFE._slot			= slot		# Remember our slot.

	@property
	def slot(thisFE):
		return thisFE._slot

	@property
	def image(thisFE):

		image = thisFE._image

		if image is None:
			name = thisFE._name
			_logger.warn(f"FieldElement.image(): Field element {name} has no image yet.")
		
		return image


class TheFieldHeader: pass


@singleton
class TheFieldHeader(FieldElement_):
	
	"""This is a special field element that displays a "header bar" that is 
		(semi-) permanently located at the top of the entire field."""

		# Need to get this from sys config instead.
	bgChar = "="	# Fill top line with this character.
	
		# Need to get this from sys config instead.
	fieldTitle = "GLaDOS Main Screen / GPT-3 Receptive Field"
			# Except, fetch "GPT-3" from the name of the cognitive system's 
			# associated language model.

	fieldTitle = ' ' + fieldTitle + ' '		# Add some padding on both sides.
	
		# Set the header width to the current value of nominal field width setting.
	headerWidth = TheFieldSettings.nominalWidth
	
		# Calculate where to place title string to (roughly) center it.
	titlePos = int((headerWidth - len(fieldTitle))/2)
	
		# Construct the full text string for the header bar.
	headerStr = overwrite('/' + bgChar*(headerWidth-2) + '\\', titlePos, fieldTitle) + '\n\n'
			# Note we add an extra newline at the end to give some vertical whitespace.

	def __init__(newHeaderElem:TheFieldHeader, *args, **kwargs):

		nhe = newHeaderElem

			#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			#| First, we call the superclass initializer to do general initial-
			#| ization for all field elements.

		super(TheFieldHeader.__wrapped__, nhe).__init__(
				"Field Header", PINNED_TO_TOP, *args, **kwargs)
			# NOTE: We always pin the field header to the very top of the 
			# receptive field, because that's where it's supposed to appear, 
			# by definition.

			# Save it as our instance image.
		nhe._image = nhe.headerStr


class ThePromptSeparator: pass

@singleton
class ThePromptSeparator(FieldElement_):
	
	"""This is a special field element that is (semi-) permanently located at 
		the top of the entire field."""
	
	bgChar = "#"	# Fill separator row with this character.
	
		# "Instructions" to embed in the separator bar.
	sepInstrs = "Enter a command line or free-form text. (/Help)"
		# Except, fetch "GPT-3" from the name of the cognitive system's 
		# associated language model.
	sepInstrs = ' ' + sepInstrs + ' '		# Add some padding on both sides.
		
		# Set the separator bar width to the current value of nominal field width setting.
	sepBarWidth = TheFieldSettings.nominalWidth
		# Quick default for now.
	
		# Calculate where to place title string to (roughly) center it.
	instrPos = int((sepBarWidth - len(sepInstrs))/2)
	
		# Construct the full text string for the topper row.
	sepBarStr = overwrite('|' + bgChar*(sepBarWidth-2) + '|', instrPos, sepInstrs) + '\n'
	
	def __init__(psElem:ThePromptSeparator, *args, **kwargs):
			# Mostly handled by FieldElement_ superclass, except that we specify
			# the element placement.

		super(ThePromptSeparator.__wrapped__, psElem).__init__(
				"Prompt Separator", PINNED_TO_BOTTOM, *args, **kwargs)
			# NOTE: We always pin the prompt separator to the bottom of the 
			# receptive field, except this will really end up being just above
			# the actual prompt area, which should have been previously pinned.

		psElem._image = '\n' + psElem.sepBarStr
			# The extra newline above is just to help it stand out, and
			# make sure it starts at the start of the line.


class TheInputArea: pass

class TheReceptiveField: pass

@singleton
class TheInputArea(FieldElement_):

	"""This is a field element that provides a space where the AI's input prompt 
		appears, and where, conceptually, the AI is 'typing' its input in response."""
		
	eventFormat = DateEventFormat		# Format for displaying the working "input event."
		# Note this format shows the current date and the entity ID.
	
	def __init__(inputArea:TheInputArea, field:TheReceptiveField, personaEntity:AI_Persona):
		
		"""Initializer for the singleton instance of the "input area" field element."""
	
		aiTextEvent = TextEvent("", personaEntity, inputArea.eventFormat)
			# This creates a fresh working draft of an "AI text event".  The 
			# initial text content of the event is the empty string.  The author
			# of the event is designated to be the AI persona that we are asking
			# the AI to take on the role of.  We use the default event format for
			# this class, which is a prompted format with the date and entity ID.

			# Store the event for later reference.
		inputArea._aiTextEvent = aiTextEvent
		
		super(TheInputArea.__wrapped__, inputArea).__init__(
			"Input Area", PINNED_TO_BOTTOM, field)
			# NOTE: The input area must be pinned to the very bottom of the receptive
			# field, so that the AI will perceive the prompt as what it's completing.

	@property
	def image(inputArea:TheInputArea):
	
		"""This standard field element property gives the (textual) image of the 
			element.  For an input area element, we just ask the AI text event to
			display itself, which renders it using its default format."""
			
		return inputArea._aiTextEvent.display()
		

class TextEventElement: pass
class TextEventElement(FieldElement_):

	"""A text event element is a field element specifically to show an individual
		text event that occurred.  These events are slid to bottom and left floating,
		that is, they are not anchored, so, they are free to pass up the field and
		disappear out of sight when the field gets too full."""

	lock = RLock()

	seqNo = 0

	def __init__(newTextEventElement:TextEventElement, field:TheReceptiveField, event:TextEvent):

		teElem = newTextEventElement

		_logger.debug(f"textEventElement.__init___(): Initializing new text event field element for text event '{event.text}'.")

		teElem._textEvent = event

		# Thread-safely increment class's sequence counter.
		with teElem.lock:
			seqno = teElem.seqNo
			teElem.seqNo = seqno + 1

		# General field element initialization.
		super(TextEventElement, teElem).__init__(
			f"Text Event #{seqno}", SLIDE_TO_BOTTOM, field)
			# NOTE: We slide new text events to the bottom (above anchored elements),
			# but then allow them to subsequently float upwards.

	@property
	def image(thisTextEventElement:TextEventElement):

		"""Standard field element property to get the element's image.
			We do this by just asking the text event to display itself."""

		teElem = thisTextEventElement

		return '\n' + teElem._textEvent.display()


class WindowElement(FieldElement_):

	"""This is a field element for containing a window."""

	def __init__(newWinElem, field, win):

		wElem = newWinElem	# Shorter name for this field element.
		wElem.win = win		# Remember the window we're holding.

		where = win.placement

		_logger.debug("winElem.__init__(): Initializing field element to contain "
					  f"window '{win.title}' with placement '{where}',")

		super(WindowElement, wElem).__init__(
			f"Window '{win.title}'", win.placement, field)

	@property
	def image(thisWinElem):

		"""Standard field element property to get the element's image.
			For window field elements, just return a view of the window's
			image data structure."""

		wElem = thisWinElem			# Shorter name for this field element.
		win = wElem.win				# Get the actual window this element is holding.
		imageObj = win.image		# This is a WindowImage object with a raw image data structure.
		viewTxt = imageObj.view()	# This asks that object for its content as a single string.

		return viewTxt	# Returns the view text as the image string for this field element.
