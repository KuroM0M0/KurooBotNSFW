import discord
import textwrap
from discord import app_commands
from discord.ext import commands
from functions.Methoden import *



class Help(commands.Cog):
    async def command_autocomplete(self, interaction: discord.Interaction, current: str,) -> list[app_commands.Choice[str]]:
        befehle = ['setup', 'settings', 'spark']
        
        # Filtert die Liste basierend auf dem, was der Nutzer bereits tippt
        return [
            app_commands.Choice(name=befehl, value=befehl)
            for befehl in befehle if current.lower() in befehl.lower()
        ]
    
    @app_commands.command(name="help", description="Zeigt dir alle Befehle an")
    async def help(self, interaction: discord.Interaction, command: str = None):
        if interaction.guild is not None:
            serverID = str(interaction.guild.id)
            CheckServerExists(serverID)

        if command is None:
            embed = discord.Embed(
                color=0x005b96
            )

            embed.add_field(
                name="ℹ️ Befehle: ",
                value=cmdDescription,
                inline=False
            )
            await interaction.response.send_message(embed=embed)
        elif command == "spark":
            await helpSpark(interaction)
        elif command == "stats":
            await helpStats(interaction)
        elif command == "settings":
            await helpSettings(interaction)
        elif command == "streak":
            await helpStreak(interaction)
        elif command == "reveal":
            await helpReveal(interaction)
        elif command == "setup":
            await helpSetup(interaction)
        elif command == "vote":
            await helpVote(interaction)
        elif command == "shop":
            await helpShop(interaction)

    @help.autocomplete('command')
    async def help_autocomplete(self, interaction: discord.Interaction, current: str):
        return await self.command_autocomplete(interaction, current)



cmdDescription = textwrap.dedent(
        "**/sparknsfw (Person)**\n"
        "Damit kannst du einer Person ein Anonymes kompliment machen.\n\n"
        #"**/stats (Person)**\n"
        #"Zeige alle Komplimente an, die diese Person bisher bekommen hat\n\n"
        #"**/topserver**\n"
        #"Zeigt die 5 meistgenutzten Server an\n\n"
        "**/feedback**\n"
        "Öffnet ein Formular in dem du Feedback für den Bot eingeben kannst\n\n"
        "**/settings**\n"
        "Stell einige Dinge ein, zb. ob du private Nachrichten möchtest\n\n"
        #"**/streak**\n"
        #"Schaue dir alle relevanten Dinge zu deiner Streak an\n\n"
        "**/profil**\n"
        "Zeigt dir Infos über dich an\n\n"
        #"**/reveal**\n"
        #"Lasse dir anzeigen von wem ein Spark gesendet wurde\n\n"
        #"**/shop**\n"
        #"Zeige dir alles was du kaufen kannst\n\n"
        #"**/inventar**\n"
        #"Hier siehst du alle Items die du besitzt.\n\n"
        #"**/use (Item)**\n"
        #"Benutze ein Item\n\n"
        )

async def helpSpark(interaction):
    embed = discord.Embed(
        color=0x005b96)
    text = textwrap.dedent( "\n\n Du kannst täglich **einer** Person einen anonymen Spark schicken. \n\n"
                            "**Wenn du oder der Server Premium hat,** kannst du **unendlich viele** verwenden. "
                            "\n\n**/sparknsfw (Person)**\n" "Es öffnet sich ein Formular in dem du die Art des Sparks und die Anonymität einstellen kannst.\n"
                            "Wenn du bei dem Feld Anonym 'Nein' auswählst, **sieht jeder dass der Spark von dir kommt.**\n"
                            "Wenn du möchtest, dass **nur der Empfänger** sieht von wem es kommt, **dann wähle 'Halb'** aus.")
    embed.add_field(
        name="Hilfe zu /spark: ",
        value=text,
        inline=False)
    await interaction.response.send_message(embed=embed)



async def helpStreak(interaction):
    embed = discord.Embed(
        color=0x005b96)
    text = textwrap.dedent("Hier siehst du alle relevanten Infos zu deiner Streak. \n"
                           "Jedes mal wenn deine Streak durch 3 teilbar ist, gibt es einen Streakpunkt."
                           "Mit Streakpunkten kannst du dir im Shop Premium kaufen.")
    embed.add_field(
        name="Hilfe zu /streak: ",
        value=text,
        inline=False)
    await interaction.response.send_message(embed=embed)


async def helpSettings(interaction):
    embed = discord.Embed(
        color=0x005b96)
    text = textwrap.dedent("Hier kannst du deine Einstellungen anpassen. \n"
                           "Es wird dir angezeigt was deine aktuellen Einstellungen sind.\n"
                           "Wenn du **kein Premium** hast, hast du **nicht die Option alles einzustellen**. \n"
                           "Was du nicht einstellen kannst, ist unter 'Premium Einstellungen' aufgelistet.")
    embed.add_field(
        name="Hilfe zu /settings: ",
        value=text,
        inline=False)
    await interaction.response.send_message(embed=embed)


async def helpStats(interaction):
    embed = discord.Embed(
        color=0x005b96)
    text = textwrap.dedent("Um deine **eigenen Stats** anzusehen, kannst du **/stats** eingeben. Du kannst zwischen Globalen und Server Stats wechseln.\n"
                           "Der Befehl zeigt dir alle Komplimente (auch custom Nachrichten) an und wie oft du diese bekommen hast."
                           "\n\n **Mit Premium** kannst du mit dem Befehl **/spark_ausblenden** custom Nachrichten ausblenden wenn du die SparkID angibst."
                           "Die SparkID findest du bei deinen Stats neben der custom Nachricht in Klammern. ")
    embed.add_field(
        name="Hilfe zu /stats: ",
        value=text,
        inline=False)
    await interaction.response.send_message(embed=embed)


async def helpReveal(interaction):
    embed = discord.Embed(
        color=0x005b96)
    text = textwrap.dedent( "Wenn jemand einen Spark macht, kann am Ende noch reveal als True angegeben werden.\n\n"
                            "Mit dem Befehl **/reveal** kannst du sehen, **welche Sparks** du aufdecken kannst.\n"
                            "Mit **/reveal (SparkID)** verwendest du einen Reveal und erfährst, von wem der Spark stammt.\n"
                            "Du brauchst dazu einen Reveal (wie viele du hast, siehst du mit /profil).\n\n"
                            "**Preise:**\n"
                            "2 Reveals = 3€\n"
                            "([3€ über **Freunde&Familie** (sonst funktioniert es nicht) senden und deine Discord ID angeben](https://www.paypal.com/paypalme/KuroPixel?country.x=DE&locale.x=de_DE))\n"
                            "1 Reveal = 40 Votepunkte (/shop)\n"
                            "\n In Zukunft ist noch geplant, dass man den Sender anfragen kann, ob es revealed werden darf.")
    embed.add_field(
        name="Hilfe zu /reveal: ",
        value=text,
        inline=False)
    await interaction.response.send_message(embed=embed)


async def helpSetup(interaction):
    embed = discord.Embed(
         color=0x005b96)
    text = textwrap.dedent("Um einen Channel festzulegen, in dem der Bot verwendet werden darf,"
                            "kannst du den Befehl **-setNSFWSparkChannel** in dem gewünschten Kanal eingeben."
                            "Es werden Administrator Berechtigungen dafür benötigt."
                            "Wenn kein Channel festgelegt wurde, funktioniert der Bot überall.\n\n"
                            "Mit **-settings** kannst du Serverweite Einstellungen treffen."
                            "\n Aktuell kannst du damit einstellen, was bei dem Anonym Feld ausgewählt werden kann."
                            "\n 0 = Ja/Halb/Nein   |   1 = Ja/Halb")
    embed.add_field(
        name="Hilfe zur Einrichtung vom Bot: ",
        value=text,
        inline=False)
    await interaction.response.send_message(embed=embed)


async def helpVote(interaction):
    embed = discord.Embed(
        color=0x005b96)
    text = textwrap.dedent("Um an VotePunkte zu kommen, kannst du alle 12 Stunden einmal Voten.\n"
                           "Wichtig dabei ist, dass du nach dem Voten nocheinmal /vote eingeben musst, um deinen Votepunkt zu erhalten."
                           "Mit diesen Punkten kannst du dir im /shop Items kaufen :)")
    embed.add_field(
        name="Hilfe zu /vote: ",
        value=text,
        inline=False)
    await interaction.response.send_message(embed=embed)


async def helpShop(interaction):
    embed = discord.Embed(
        color=0x005b96)
    text = textwrap.dedent("Um dir Items zu kaufen, kannst du den Befehl **/shop** eingeben.\n"
                           "Dort siehst du auch direkt wie viele VotePunkte und StreakPunkte du hast.\n"
                           "Was die Items genau machen, musst du selbst herausfinden :)\n")
    embed.add_field(
        name="Hilfe zu /shop: ",
        value=text,
        inline=False)
    await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
    print("HelpCommand geladen ✅")