import discord
from discord.ext import commands
from dataBase import *
from config import connection
from Methoden import CheckServerExistsInSettings



def buildEmbed(ctx):
        embed = discord.Embed(title="Einstellungen", color=0x005b96)
        embed.add_field(
            name="🔒 Anonymität Auswahlmöglichkeiten",
            value=f">>> `Hug/Pat` → {getServerAnonymHug(connection, ctx.guild.id)}\n"
                  f"`Sparks` → {getServerAnonymSpark(connection, ctx.guild.id)}",
            inline=False
        ) 
        return embed

class ServerSettings(commands.Cog):
    @commands.command(name="settings")
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        serverID = ctx.guild.id
        CheckServerExistsInSettings(serverID)
        premium = getServerPremium(connection, serverID)
        embed = buildEmbed(ctx)
        await ctx.send(embed=embed, view=ServerSettingsView(premium, serverID))

    


class ServerSettingsSelect(discord.ui.Select):
    def __init__(self, hatPremium, serverID):
        self.serverID = serverID
        self.hatPremium = hatPremium
        options = [
                discord.SelectOption(label="Der Server hat kein Premium!", description="Um etwas umstellen zu können, benötigt der Server Premium!", value="noPremium", emoji="⛔")
            ]
        
        if hatPremium:
            options.append(discord.SelectOption(label="Hug", description="Stelle ein, was die User auswählen dürfen.", value="hug", emoji="⛔"))
            options.append(discord.SelectOption(label="Spark", description="Stelle ein, was die User auswählen dürfen.", value="spark", emoji="⛔"))
            options.remove(options[0])
            
        #else: #Damit bei Premium alles in richtiger Reihenfolge angezeigt wird
            #options.append(discord.SelectOption(label="Ping", description="Stelle ein, ob du Pings erhalten möchtest", value="Ping", emoji=""))
            
            
        super().__init__(placeholder="Einstellungen ändern", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        serverID = self.serverID
        value = self.values[0]  # der ausgewählte Wert
        locale = interaction.locale

        # ----- Umschalt-Logik -----
        if value == "hug":
            val = getServerAnonymHug(connection, serverID)
            setServerAnonymHug(connection, serverID, not val)

        elif value == "spark":
            val = getServerAnonymSpark(connection, serverID)
            setServerAnonymSpark(connection, serverID, not val)

        # ----- Embed neu aufbauen -----
        settingsObj = buildEmbed(interaction)
        await interaction.response.edit_message(embed=settingsObj, view=self.view)



class ServerSettingsView(discord.ui.View):
    def __init__(self, hatPremium: bool, serverID: int):
        super().__init__(timeout=60)
        self.add_item(ServerSettingsSelect(hatPremium, serverID))

async def setup(bot):
    await bot.add_cog(ServerSettings(bot))
    print("ServerSettings geladen ✅")