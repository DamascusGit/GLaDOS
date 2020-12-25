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


from	infrastructure.decorators	import	singleton
from	.placement					import	Placement
	
global __all__
__all__ = [
		'FieldElement_',
		'TheFieldHeader',
		'ThePromptSeparator',
	]

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

	def __init__(thisFE, where:Placement=None):
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
			# Remember our initial requested placement.
		thisFE._initPlacement	= where
	
@singleton
class TheFieldHeader(FieldElement_):
	
	"""This is a special field element that displays a "header bar" that is 
		(semi-) permanently located at the top of the entire field."""
	
		# Need to get this from sys config instead.
	bgChar = "*"	# Fill top line with this character.
	
		# Need to get this from sys config instead.
	fieldTitle = "GLaDOS Main Screen / GPT-3 Receptive Field"
		# Except, fetch "GPT-3" from the name of the cognitive system's 
		# associated language model.
	fieldTitle = ' ' + fieldTitle + ' '		# Add some padding on both sides.
			
	headerWidth = _DEFAULT_NOMINAL_WIDTH
		# Quick default for now.
	
		# Calculate where to place title string to (roughly) center it.
	titlePos = int((headerWidth - len(fieldTitle))/2)
	
		# Construct the full text string for the topper bar.
	headerStr = overwrite(bgChar*headerWidth, titlePos, fieldTitle) + '\n'
	
	def __init__(theFieldHeader, *args, **kwargs):
			# Mostly handled by FieldElement_ superclass, except that we specify
			# the element placement.
		super(TheFieldTopper, theFieldHeader).__init__(Placement.PINNED_TO_TOP, *args, **kwargs)
			# NOTE: We always pin the field topper to the very top of the 
			# receptive field, because that's where it's supposed to appear, 
			# by definition.

	@property
	def image(theFieldHeader):		# Just a constant string.
		return topperStr
		# NOTE: Later we might want to modify this to be able to be updated
		# dynamically, e.g., if the ai config is reloaded, and the new config
		# has a different NLP model name.

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
		
	sepBarWidth = _DEFAULT_NOMINAL_WIDTH
		# Quick default for now.
	
		# Calculate where to place title string to (roughly) center it.
	instrPos = int((topperWidth - len(sepInstrs))/2)
	
		# Construct the full text string for the topper row.
	sepBarStr = overwrite(bgChar*sepBarWidth, instrPos, sepInstrs) + '\n'
	
	def __init__(thePromptSeparator, *args, **kwargs):
			# Mostly handled by FieldElement_ superclass, except that we specify
			# the element placement.
		super(ThePromptSeparator, thePromptSeparator).__init__(Placement.PINNED_TO_BOTTOM, *args, **kwargs)
			# NOTE: We always pin the prompt separator to the bottom of the 
			# receptive field, except this will really end up being just above
			# the actual prompt area, which should have been previously pinned.

	@property
	def image(thePromptSeparator):		# Just a constant string.
		return sepBarStr
		# NOTE: Later we might want to modify this to be able to be updated
		# dynamically, like in the config file.  Not done yet.
