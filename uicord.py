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

class View(ui.View):
	def __init__(self):
		super().__init__()

	def add(self, component):
		self.add_item(component)
		return component
	async def reload(self, ctx):
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

class Text(ui.Button):
	def __init__(self, text="My Text", emoji=None):
		super().__init__(emoji=emoji, label=text)
		self._underlying.disabled = False
		self._underlying.style = Colors.Gray
	async def callback(self, ctx, *args):
		await self.view.reload(ctx)
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

class ButtonRow(ButtonChoices):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	async def callback(self, *args):
		await self.cb(*args)
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

class Button(ui.Button):
	def __init__(self, text="My Button", emoji=None, color=Colors.Blue, url=None):
		super().__init__()
		self.label=text
		self.color = color if not url else Colors.link
		self.emoji = emoji
	@property
	def color(self): return self.style
	@color.setter
	def color(self, value): self.style=value
