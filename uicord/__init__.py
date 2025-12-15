import discord.ui as ui
from discord import enums
from discord import SelectOption
import inspect

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
		await ctx.response.edit_message(view=self)

def interaction(component=None):
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
	def __init__(self, text="myText"):
		super().__init__(text)

class ButtonChoices(ui.ActionRow):
	def __init__(self, *btns):
		super().__init__()
		self.btns = []
		self.saved_colors=[]
	async def cb(self, ctx, option):
		await ctx.response.edit_message(view=self.view)
	async def callback(self, ctx):
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
		self.btns.append(button)
		button.custom_id=button.label+"_id"
		button.callback = self.callback
		button.active=False
		self.add_item(button)
		self.saved_colors.append(button.color)

class ActionRow(ui.ActionRow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	def add(self, *a, **k): self.add_item(*a,**k)
class Choices(ui.Select):
	def __init__(self, placeholder="Pick"):
		super().__init__()
		self.placeholder=placeholder
	def add(self, 
		option="Option", 
		emoji=None,
		description=None,
		default=False
	):
		self.options.append(
			SelectOption(
				label=option,
				emoji=emoji,
				description=description,
				default=default,
				value=option.replace(" ","-").lower()
			)
		)
	@property
	def picked(self):
		return self.values[0]
	async def force(self, index):
		selected = self.options[index%len(self.values)]
		for opt in self.options:
			opt.default = (selected==opt)
		self.disabled = True
	async def disable(self, v=True):
		selected = self.values[0]
		for opt in self.options:
			opt.default = (selected==opt.value)
		self.disabled = v
	async def update(self):
		self.disable(False)

class Button(ui.Button):
	def __init__(self, text="My Button", emoji=None, color=Colors.Blue, url=None, id=None):
		super().__init__(label=text, custom_id=id, style=color, url=url)
		self.emoji = emoji
	@property
	def color(self): return self.style
	@color.setter
	def color(self, value): self.style=value
class Toggle(Button):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.active=False
		self.style=Colors.Red
		self.emoji="❌"

	async def callback(self, ctx):
		if active:
			self.style=Colors.Red
			self.emoji="❌"
		else:
			self.style=Colors.Green
			self.emoji="✅"
		self.active is not active
		await self.cb(ctx)

class Container(ui.Container):
	def __init__(self, *items, **kwargs):
		super().__init__(*items, **kwargs)

class Separator(ui.Separator):
	def __init__(self, *, divider=True):
		super().__init__(divider=divider)

class Thumbnail(ui.Thumbnail):
	def __init__(self, url):
		super().__init__(url)

class Section(ui.Section):
	def __init__(self, *items, **kwargs):
		super().__init__(*items, **kwargs)


class Modal(ui.DesignerModal):
	def __init__(self, title="Modal Title"):
		super().__init__(title=title)
		self.inputs=[]
	def add_input(self, label="input label", style="short", placeholder=None, default=None):
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
		pass
	async def get_value(self, index=0):
		return self.inputs[index].value
