import discord.ui as ui
import discord
from discord import enums
from discord import SelectOption
import inspect, functools

class Colors:
	Green = 3
	Blue = 1
	Gray = 2
	Grey = 2
	Red = 4
	Link = 5
	Yellow = 6

class View(ui.DesignerView):
	"""The main container of every component."""
	def __init__(self):
		"""Initializes the view"""
		super().__init__()

	def add(self, component):
		"""
		The component specified to the view

		:param component: The component to be added
		:return: Returns the component added.
		"""
		self.add_item(component)
		return component
	async def reload(self, ctx):
		"""
		Reloads the current view, Updates every unsynced compoenents.

		:return: None
		"""
		try:
			await ctx.response.defer()
		except discord.errors.InteractionResponded:
			await ctx.edit_original_response(view=self)

def interaction(component=None):
	"""
	Decorator to set a callback.

	:param component: The component to be assigned a callback.
	:return: None
	"""
	def wrapper(func):
		if not component:
			raise TypeError("Interaction needs a component")
		if not inspect.iscoroutinefunction(func):
			raise TypeError(f"{component.__class__.__name__} Interaction MUST be asynchronous")
		async def interact(*args):
			try:
				await func(*args)
			except Exception as e:
				print(f"\033[31m{e}",end="\033[0m\n")
				await args[0].respond(f"Error found while interacting with: {component.__class__.__name__}")
		if not isinstance(component, (Toggle, Text, ButtonChoices)):
			component.callback = interact
		else:
			component.cb = interact
	return wrapper

class Text(ui.TextDisplay):
	"""
	Text display for View and Modal.
	"""
	def __init__(self, text="myText"):
		"""
		The text initializer.

		:param text: Text to be displayed
		"""
		super().__init__(text)

class ButtonChoices(ui.ActionRow):
	"""
	Simple Radio Buttons
	"""
	def __init__(self, *btns):
		super().__init__()
		self.btns = []
		self.saved_colors=[]
	async def cb(self, ctx):
		"""
		Default callback for button click.

		:param ctx: The interaction context.
		"""
		await ctx.response.edit_message(view=self.view)
	async def callback(self, ctx):
		"""
		The core callback to make Buttons work.

		:param ctx: The interaction context
		"""
		pressed = ctx.data["custom_id"]
		for i, btn in enumerate(self.btns):
			if btn.custom_id == pressed:
				if btn.active:
					btn.style=self.saved_colors[i]
					self.picked = None
					btn.active=False
				else:
					btn.style = Colors.Green if self.saved_colors[i]!=Colors.Green else Colors.Red
					self.picked = btn.label
					btn.active=True
			else:
				btn.style = self.saved_colors[i]
				btn.active=False
		await self.cb(ctx)
	def add(self, button):
		"""
		Adds a button to the ButtonChoices

		:param button: The button to be added.
		"""
		self.btns.append(button)
		button.custom_id=button.label+"_id"
		button.callback = self.callback
		button.active=False
		self.add_item(button)
		self.saved_colors.append(button.color)

class ActionRow(ui.ActionRow):
	"""
	Regular PyCord ActionRow
	"""
	def __init__(self, *args, **kwargs):
		"""
		Creates the action row.

		:param args: Args
		:param kwargs: Kwargs
		"""
		super().__init__(*args, **kwargs)
	def add(self, *a, **k):
		"""
		Macro for add_item()

		:param a: Arguments.
		:param k: Keyword Arguments.
		"""
		self.add_item(*a,**k)
class Choices(ui.Select):
	"""
	Options menu
	"""
	def __init__(self, type=discord.ComponentType.string_select, placeholder="Pick"):
		"""
		Creates a new select menu

		:param placeholder: The text that is shown if no option is picked.
		"""
		super().__init__(type)
		self.placeholder=placeholder
		self.component_type=type
		self.DEFAULTOPTION=None
	def add(self, 
		option="Option", 
		emoji=None,
		description=None,
		default=False
	):
		"""
		Adds a new select option.

		:param option: The text displayed
		:param emoji: The emoji of the text
		:param description: The description of the choice.
		:param default: If the input is default.
		"""
		option=SelectOption(
			label=option,
			emoji=emoji,
			description=description,
			default=default,
			value=option.replace(" ","-").lower()
		)
		self.append_option(option)

		if default:
			self.DEFAULTOPTION=option
	@property
	def picked(self):
		"""
		The option picked by the user.
		"""
		if not self.values:
			if self.DEFAULTOPTION:
				return self.DEFAULTOPTION.value
			return None
		return self.values[0]
	async def force(self, index):
		"""
		Force pick an option by index 
		DEPRECATED: NO LONGER SUPPORTED.
		ANY CALL OF THIS METHOD NO LONGER WORKS.

		:param index: The index to be forced
		"""
		return
	async def disable(self, v=True):
		"""
		Disables the select menu and updates.

		:param v: Disabled or not.
		"""
		if self.component_type!=discord.ComponentType.channel_select:
			selected = self.picked
			if selected:
				for opt in self.options:
					opt.default = (selected==opt.value)
		self.disabled = v
	async def update(self):
		"""
		Updates the select menu buffer.
		"""
		if self.component_type!=discord.ComponentType.channel_select:
			await self.disable(False)
	async def callback(self, ctx):
		"""
		Default callback to update select menus.

		:param ctx: Interaction context
		"""
		await self.update()
		await self.view.reload(ctx)

class Button(ui.Button):
	"""
	Interactable Button.
	"""
	def __init__(self, text="My Button", emoji=None, color=Colors.Blue, url=None, id=None):
		"""
		Initial function for the button.

		:param text: The text to be displayed
		:param emoji: The emoji for the button
		:param color: The color of the button
		:url: The url if its a link.
		:id: The custom id for the button
		"""
		super().__init__(label=text, custom_id=id, style=color, url=url)
		self.emoji = emoji
	@property
	def color(self):
		"""
		The color of the Button.
		"""
		return self.style
	@color.setter
	def color(self, value): self.style=value
class Toggle(Button):
	"""
	Toggle button.
	"""
	def __init__(self, *args, **kwargs):
		"""
		The init function
		"""
		super().__init__(*args, **kwargs)
		self.active=False
		self.style=Colors.Red
		self.emoji="❌"

	async def callback(self, ctx):
		"""
		Core callback of the button

		:param ctx: The interaction context
		"""
		if active:
			self.style=Colors.Red
			self.emoji="❌"
		else:
			self.style=Colors.Green
			self.emoji="✅"
		self.active is not active
		await self.cb(ctx)

class Container(ui.Container):
	"""
	Regular Discord Container
	"""
	def __init__(self, *items, **kwargs):
		super().__init__(*items, **kwargs)

class Separator(ui.Separator):
	"""
	Regular Discord Separator
	"""
	def __init__(self, *, divider=True):
		super().__init__(divider=divider)

class Thumbnail(ui.Thumbnail):
	"""
	Regular Discord Thumbnail
	"""
	def __init__(self, url):
		super().__init__(url)

class Section(ui.Section):
	"""
	Regular Discord Section
	"""
	def __init__(self, *items, **kwargs):
		super().__init__(*items, **kwargs)


class Modal(ui.DesignerModal):
	"""
	The main input/output system for components.
	"""
	def __init__(self, title="Modal Title"):
		"""
		Creates the modal

		:param title: Title of the modal
		"""
		super().__init__(title=title)
		self.inputs=[]
	def add_input(self, label="input label", style="short", placeholder=None, default=None):
		"""
		Adds a new input

		:param label: The button label
		:param style: Style of the input ("short" or "long")
		:param placeholder: The text displayed if nothing is inputted.
		:param default: The default text.
		"""
		inp_style = enums.InputTextStyle.short if style=="short" else enums.InputTextStyle.paragraph
		input_text = ui.InputText(style=inp_style, placeholder=placeholder, value=default)
		self.add_item(
			ui.Label(
				label=label,
				item=input_text
			)
		)
		self.inputs.append(input_text)
		return input_text
	async def callback(self, ctx):
		"""
		Calls when modal is submitted.

		:param ctx: The interaction context
		"""
		pass
	async def get_value(self, index=0):
		"""
		Gets the value of a text input by index

		:param index: Index of the text input.
		"""
		return self.inputs[index].value
