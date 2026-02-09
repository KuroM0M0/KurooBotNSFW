import discord
from datetime import datetime
from discord import app_commands, ui
from discord.ext import commands
from Methoden import replaceEmotes, getUserName
from dataBase import *
from config import connection 


class RevealCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reveal", description="Lasse dir anzeigen von wem ein Spark gesendet wurde!")
    async def reveal(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        userID = str(interaction.user.id)

        # Grunddaten abrufen
        reveals = getReveals(connection, userID)
        revealedRaw = getRevealedSparks(connection, userID) #Tupple können nicht verändert werden, deswegen in Liste umwandeln
        revealed = []
        for row in revealedRaw:
            sparkID, timestamp, sparkText, senderID = row
            try:
                userName = await getUserName(senderID, self.bot)
            except:
                userName = "Unbekannter Nutzer"
            revealed.append((sparkID, timestamp, sparkText, userName))

        # --- LOGIK FÜR EINE SPEZIFISCHE ID ---
        #soll von Item übernommen werden
        """if sparkid is not None:
            isRevealed = getIsRevealed(connection, sparkid)

            if revealUses < 1:
                await interaction.followup.send("Du hast keine Reveals mehr. Um dir neue zu holen, gib '/help reveal' ein.", ephemeral=True)
                return

            if userID != getSparkTargetID(connection, sparkid):
                await interaction.followup.send("Du kannst nur Sparks revealen, die du selbst erhalten hast!", ephemeral=True)
                return

            result = getSparkReveal(connection, sparkid)
            if result is None:
                await interaction.followup.send("Dieser Spark existiert nicht oder der Sender möchte Anonym bleiben.", ephemeral=True)
                return
            elif isRevealed:
                await interaction.followup.send(f"Dieser Spark wurde bereits von dir aufgedeckt!", ephemeral=True)
                return
            else:
                await interaction.followup.send(f"Dieser Spark wurde von {result} gesendet.", ephemeral=True)
                setRevealUses(connection, userID, revealUses - 1)
                setIsRevealed(connection, sparkid)

        # --- LOGIK FÜR DIE ÜBERSICHT ---
        else:"""
            # Wir nutzen hier die buildMainEmbed Funktion aus deiner reveal.py Datei!
        embed = buildMainEmbed(reveals, revealed, interaction)
            
            # Wir nutzen die RevealMainView aus deiner reveal.py
        view = RevealMainView(reveals, revealed)
            
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)




class RevealMainView(ui.View):
    def __init__(self, normal_reveals, revealed):
        super().__init__(timeout=None)
        self.normal_reveals = normal_reveals
        self.revealed = revealed
        """self.custom_reveals = custom_reveals
        self.revealed_custom = revealed_custom

    @ui.button(label="Custom Sparks", style=discord.ButtonStyle.primary)
    async def show_custom(self, interaction: discord.Interaction, button: ui.Button):
        # Wechsel zu Custom-View
        custom_embed = buildCustomEmbed(self.custom_reveals, self.revealed_custom, interaction)
        await interaction.response.edit_message(embed=custom_embed, view=RevealCustomView(
            self.normal_reveals, self.revealed, self.custom_reveals, self.revealed_custom
        ))


class RevealCustomView(ui.View):
    def __init__(self, normal_reveals, revealed, custom_reveals, revealed_custom):
        super().__init__(timeout=None)
        self.normal_reveals = normal_reveals
        self.revealed = revealed
        self.custom_reveals = custom_reveals
        self.revealed_custom = revealed_custom

    @ui.button(label="Zurück", style=discord.ButtonStyle.secondary)
    async def back_to_main(self, interaction: discord.Interaction, button: ui.Button):
        # Wechsel zurück zur Haupt-View
        main_embed = buildMainEmbed(self.normal_reveals, self.revealed, interaction)
        await interaction.response.edit_message(embed=main_embed, view=RevealMainView(
            self.normal_reveals, self.revealed, self.custom_reveals, self.revealed_custom
        ))"""





def revealEmbed(revealed):
    descLines = []
    for spark_id, timestamp, compliment, sender_name in revealed:
        try:
            dt = datetime.fromisoformat(timestamp)
            unix_ts = int(dt.timestamp())
        except ValueError:
            unix_ts = 0
        line = f"{compliment} — <t:{unix_ts}:R> — von **{sender_name}** — ID `{spark_id}`"
        descLines.append(line)
    return descLines


def buildMainEmbed(reveals, revealed, interaction):
    description_lines = []

    if revealed:
        description_lines.append("**Bereits revealed:**")
        for spark_id, timestamp, compliment, sender_name in revealed:
            compliment = replaceEmotes(compliment, interaction.guild, interaction.client)
            try:
                dt = datetime.fromisoformat(timestamp)
                unix_ts = int(dt.timestamp())
            except ValueError:
                unix_ts = 0
            description_lines.append(f"{compliment} — <t:{unix_ts}:R> — von **{sender_name}** — ID `{spark_id}`")

    if reveals:
        if description_lines:
            description_lines.append("")  # Leerzeile
        description_lines.append("**Noch aufdeckbar:**")
        for spark_id, timestamp, compliment in reveals:
            compliment = replaceEmotes(compliment, interaction.guild, interaction.client)
            try:
                dt = datetime.fromisoformat(timestamp)
                unix_ts = int(dt.timestamp())
            except ValueError:
                unix_ts = 0
            description_lines.append(f"{compliment} — <t:{unix_ts}:R> — ID `{spark_id}`")

    if not description_lines:
        description_lines.append("Du hast aktuell keine aufdeckbaren Sparks.")

    return discord.Embed(
        title="✨ Aufdeckbare Sparks:",
        description="\n".join(description_lines),
        color=0x00ff00
    )


"""def buildCustomEmbed(custom_reveals, revealed_custom, interaction):
    description_lines = []

    if revealed_custom:
        description_lines.append("**Bereits revealed (Custom):**")
        for spark_id, timestamp, compliment, sender_name in revealed_custom:
            compliment = replaceEmotes(compliment, interaction.guild, interaction.client)
            try:
                dt = datetime.fromisoformat(timestamp)
                unix_ts = int(dt.timestamp())
            except ValueError:
                unix_ts = 0
            description_lines.append(f"{compliment} — <t:{unix_ts}:R> — von **{sender_name}** — ID `{spark_id}`")
            description_lines.append("────────────")

    if custom_reveals:
        if description_lines:
            description_lines.append("")  # Leerzeile
        description_lines.append("**Noch revealbar (Custom):**")
        for spark_id, timestamp, compliment in custom_reveals:
            compliment = replaceEmotes(compliment, interaction.guild, interaction.client)
            try:
                dt = datetime.fromisoformat(timestamp)
                unix_ts = int(dt.timestamp())
            except ValueError:
                unix_ts = 0
            description_lines.append(f"{compliment} — <t:{unix_ts}:R> — ID `{spark_id}`")
            description_lines.append("────────────")

    if not description_lines:
        description_lines.append("Du hast aktuell keine revealbaren Custom Sparks.")

    return discord.Embed(
        title="✨ Revealbare Sparks:",
        description="\n".join(description_lines),
        color=0x00ff00
    )"""

# Setup Funktion für das Laden des Cogs
async def setup(bot):
    await bot.add_cog(RevealCog(bot))