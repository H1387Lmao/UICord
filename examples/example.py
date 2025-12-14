from uicord import *
from discord.ext import commands
import discord

Intents = discord.Intents.default()
Intents.messages = True

bot = commands.Bot(intents=Intents, 
	command_prefix="?"
)

def Test():
	MyView = View()
	btn = MyView.add(Button("Click Me", color=Colors.Blue))

	choices = MyView.add(Choices("Choose an option"))
	choices.add("Option 1")
	choices.add("Option 2")

	btnChoices = ButtonChoices()
	btnChoices.add(Button(
		text="Btn1",
		emoji="✅",
		color=Colors.Blue
	))

	text = Text(text="Hello this is a text label!")
	MyView.add(text)

	MyView.add(btnChoices) #Need to add after adding buttons
	
	
	@interaction(component=btnChoices)
	async def btnchose(ctx):
		print(btnChoices.picked)
		await MyView.reload(ctx)

	@interaction(component=choices)
	async def changed(ctx):
		await choices.force(1)
		await MyView.reload(ctx)
	@interaction(component=btn)
	async def Yay(ctx):
		await ctx.respond("Yay you pressed my button", ephemeral=True)
	return MyView

@bot.slash_command(name="test")
async def test_btn(ctx):
	await ctx.defer()
	await ctx.send_followup(view=Test())
bot.run("BOT_TOKEN")
