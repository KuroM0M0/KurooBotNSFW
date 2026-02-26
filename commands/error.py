from discord.ext import commands
from discord import app_commands
import discord
import traceback

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
    async def onAppCommandError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        # Der eigentliche Fehler steckt bei Slash Commands oft in 'original'
        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original

        # 1. Fehlende Berechtigungen (Bot darf etwas nicht tun)
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("⚠️ Ich habe nicht genug Rechte dafür!", ephemeral=True)

        # 2. Command auf Cooldown
        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Chill mal. Versuch es in {error.retry_after:.2f}s erneut.", ephemeral=True)

        # 3. Fehlende Berechtigungen des Nutzers
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("🚫 Du darfst diesen Command nicht nutzen!", ephemeral=True)

        # 4. Der "Unbekannte" Fehler
        else:
            print(f"--- FEHLER IM COMMAND '{interaction.command.name}' ---")
            # Das hier druckt den kompletten Stacktrace (Zeilennummer, Datei, etc.)
            traceback.print_exception(type(error), error, error.__traceback__)
            
            if not interaction.response.is_done():
                await interaction.response.send_message("💥 Ein interner Fehler ist aufgetreten.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorHandler(bot))
