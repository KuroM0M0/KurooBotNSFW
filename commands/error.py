from discord.ext import commands
from discord import app_commands
import discord

class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Registriert den globalen Slash-Command-Error-Handler
        self.bot.tree.on_error = self.onAppCommandError

    # --------------------------
    # PREFIX COMMAND ERRORS
    # --------------------------
    @commands.Cog.listener()
    async def onOommandError(self, ctx: commands.Context, error: commands.CommandError):
        """Globaler Error-Handler für Prefix-Commands."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Dir fehlen die nötigen Berechtigungen für diesen Command!")
        elif isinstance(error, commands.MissingRole):
            await ctx.send(f"❌ Du benötigst die Rolle **{error.missing_role}** für diesen Command!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Fehlendes Argument: `{error.param.name}`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Ungültiges Argument übergeben!")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("❌ Du erfüllst die Voraussetzungen für diesen Command nicht.")
        elif isinstance(error, commands.CommandInvokeError):
            original_error = error.original
            await ctx.send(f"⚠️ Ein Fehler ist aufgetreten: `{type(original_error).__name__}`")
            print(f"Fehler in Prefix-Command '{ctx.command.name}': {original_error}")  # Logging
        else:
            await ctx.send("❌ Ein unbekannter Fehler ist aufgetreten. Bitte versuche es später erneut.")

    # --------------------------
    # SLASH COMMAND ERRORS
    # --------------------------
    async def onAppCommandError(self, interaction: discord.Interaction, error: Exception):
        """Globaler Error-Handler für Slash-Commands."""
        if isinstance(error, app_commands.CommandInvokeError):
            original = error.original
            if isinstance(original, discord.Forbidden):
                await interaction.response.send_message("⚠️ Ich konnte dem Nutzer keine Nachricht schicken (vermutlich blockiert oder DMs deaktiviert).")
                return
            print(f"[SlashCommand-Error] {original}")
        else:
            print(f"[Unbekannter SlashCommand-Error] {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorHandler(bot))
