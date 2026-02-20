import discord
from discord import app_commands
from discord.ext import commands
from config import connection
from functions.shop import ShopEmbed, ShopButtons


class Shop(commands.Cog):
    @app_commands.command(name="shop", description="Hier kannst du dir unterschiedliche Items mit Vote/Streakpunkten kaufen :)")
    async def shop(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = ShopEmbed(1, interaction, connection)
        try:
            await interaction.followup.send(embed=embed, view=ShopButtons(connection))
        except Exception as e:
            print("Fehler beim Senden des Shops:", e)
            await interaction.followup.send(f"Fehler: {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Shop(bot))
    print("Shop geladen ✅")