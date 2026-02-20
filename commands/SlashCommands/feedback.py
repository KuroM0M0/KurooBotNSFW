import discord
from discord import app_commands
from discord.ext import commands
from config import KuroID

class FeedbackModal(discord.ui.Modal, title="Feedback Formular"):
    feedback = discord.ui.TextInput(label="Dein Feedback", style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        bot_owner = await interaction.client.fetch_user(KuroID)
        embed = discord.Embed(title="Neues Feedback erhalten!", description=self.feedback.value, color=discord.Color.blue())
        embed.set_footer(text=f"Von {interaction.user} ({interaction.user.id})")
        
        await bot_owner.send(embed=embed)
        await interaction.response.send_message("Danke für dein Feedback :D", ephemeral=True)


class Feedback(commands.Cog):
    @app_commands.command(name="feedback", description="Sende über ein Formular Feedback an den Bot-Entwickler")
    async def feedback(self, interaction: discord.Interaction):
            await interaction.response.send_modal(FeedbackModal())


async def setup(bot: commands.Bot):
    await bot.add_cog(Feedback(bot))
    print("Feedback geladen ✅")