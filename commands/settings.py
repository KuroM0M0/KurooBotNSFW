from dataBase import *
import discord
from discord import ButtonStyle, ui
from discord.ext import commands
from main import connection, bot, localizations, translate

#secondary, grey, gray = grau
#primary, blurple = blau
#danger, red = rot
#green, success = grün
#link = link benötigt
#premium = sku_id benötigt

class newSettings(discord.ui.View):
    def __init__(self, premium: bool, userID: int, locale: Locale):
        super().__init__(timeout=60)
        self.userID = userID
        self.premium = premium
        self.locale = locale

        # Daten laden
        self.settingStuff(userID)

    # ---- Format-Helfer ----
    @staticmethod
    def format_privacy(val, locale: Locale): 
        return translate(locale, "embed.settings.format.privacy.private") if val == 1 else translate(locale, "embed.settings.format.privacy.public")

    @staticmethod
    def format_toggle(val, locale: Locale): 
        return translate(locale, "embed.settings.format.toggle.on") if val == 1 else translate(locale, "embed.settings.format.toggle.off")

    # ---- Daten laden (normal) ----
    def settingStuff(self, userID):
        self.streakPrivate = self.format_privacy(getStreakPrivate(connection, userID), locale=self.locale)
        self.statsPrivate = self.format_privacy(getStatsPrivate(connection, userID), locale=self.locale)
        self.profilPrivate = self.format_privacy(getProfilPrivateSetting(connection, userID), locale=self.locale)
        self.newsletter = self.format_toggle(getNewsletter(connection, userID), locale=self.locale)
        self.sparkDM = self.format_toggle(getSparkDM(connection, userID), locale=self.locale)
        self.Ping = self.format_toggle(getPingSetting(connection, userID), locale=self.locale)
        self.customSpark = self.format_toggle(getCustomSparkSetting(connection, userID), locale=self.locale)

    def settingEmbed(self):
        embed = discord.Embed(title="Einstellungen", color=0x005b96)

        embed.add_field(
            name="🔒 Privatsphären Einstellungen",
            value=f">>> `Streak` → {self.streakPrivate}\n"
                  f"`Profil` → {self.profilPrivate}",
            inline=False
        )

        embed.add_field(
            name="⚙️ Allgemeine Einstellungen",
            value=f">>> `Ping` → {self.Ping}",
            inline=False
        )

        embed.add_field(
            name="💎 Premium Einstellungen",
            value=f">>> `Newsletter` → {self.newsletter}\n"
                  f"`SparkDM` → {self.sparkDM}\n"
                  f"`Stats` → {self.statsPrivate}\n"
                  f"`Custom Sparks` → {self.customSpark}",
            inline=False
        )

        return embed

    # Premium-Embed (Platzhalter)
    def settingEmbedPremium(self):
        embed = discord.Embed(title="Einstellungen", color=0x005b96)
        embed.add_field(
            name="🔒 Privatsphären Einstellungen",
            value=f">>> `Streak` → {self.streakPrivate}\n"
                f"`{translate(self.locale, 'embed.settings.privacy.profil')}` → {self.profilPrivate}\n"
                f"`Stats` → {self.statsPrivate}",
            inline=False
        )
        embed.add_field(
            name="⚙️ Allgemeine Einstellungen",
            value=f">>> `Ping` → {self.Ping}\n"
                f"`Newsletter` → {self.newsletter}\n"
                f"`SparkDM` → {self.sparkDM}\n"
                f"`Custom Sparks` → {self.customSpark}",
            inline=False
        )
        return embed
    
    def getEmbed(self):
        if self.premium:
            return self.settingEmbedPremium()
        else:
            return self.settingEmbed()



class SettingSelect(discord.ui.Select):
    def __init__(self, hatPremium, userID):
        self.userID = userID
        self.hatPremium = hatPremium
        options = [
                discord.SelectOption(label="Streak", description="Stelle ein, ob deine Streak Privat oder Öffentlich angezeigt werden soll", value="streak", emoji="<:Streakpunkt:1406583255934963823>"),
                discord.SelectOption(label="Profil", description="Stelle ein, ob dein Profil Privat oder Öffentlich angezeigt werden soll", value="profil", emoji="👤")
            ]
        
        if hatPremium:
            options.append(discord.SelectOption(label="Stats", description="Stelle ein, ob deine Stats Privat oder Öffentlich angezeigt werden sollen", value="stats", emoji="📊"))
            options.append(discord.SelectOption(label="Ping", description="Stelle ein, ob du Pings erhalten möchtest", value="Ping", emoji="<:PeepoPing:1412450415986872461>"))
            options.append(discord.SelectOption(label="Newsletter", description="Stelle ein, ob du Updates vom Bot in deine DMs erhalten möchtest", value="newsletter", emoji="📰"))
            options.append(discord.SelectOption(label="SparkDM", description="Stelle ein, ob du vom Bot angeschrieben werden willst, wenn du gesparkt wurdest", value="sparkdm", emoji="<:Schaufel:1410610904361472031>"))
            options.append(discord.SelectOption(label="Custom Sparks", description="Stelle ein, ob du Custom Sparks erhalten möchtest", value="customsparks", emoji="✨"))
        else: #Damit bei Premium alles in richtiger Reihenfolge angezeigt wird
            options.append(discord.SelectOption(label="Ping", description="Stelle ein, ob du Pings erhalten möchtest", value="Ping", emoji="<:PeepoPing:1412450415986872461>"))
            
        super().__init__(placeholder="Einstellungen ändern", min_values=1, max_values=1, options=options)


    async def callback(self, interaction: discord.Interaction):
        userID = str(interaction.user.id)
        value = self.values[0]  # der ausgewählte Wert
        locale = interaction.locale

        # ----- Umschalt-Logik -----
        if value == "streak":
            val = getStreakPrivate(connection, userID)
            setStreakPrivate(connection, userID, not val)

        elif value == "profil":
            val = getProfilPrivateSetting(connection, userID)
            setProfilPrivateSetting(connection, userID, not val)

        elif value == "Ping":
            val = getPingSetting(connection, userID)
            setPingSetting(connection, userID, not val)

        elif value == "newsletter":
            val = getNewsletter(connection, userID)
            setNewsletter(connection, userID, not val)

        elif value == "sparkdm":
            val = getSparkDM(connection, userID)
            setSparkDM(connection, userID, not val)

        elif value == "stats":
            val = getStatsPrivate(connection, userID)
            setStatsPrivate(connection, userID, not val)

        elif value == "customsparks":
            val = getCustomSparkSetting(connection, userID)
            setCustomSparkSetting(connection, userID, not val)

        # ----- Embed neu aufbauen -----
        settingsObj = newSettings(self.hatPremium, userID, locale)
        await interaction.response.edit_message(embed=settingsObj.getEmbed(), view=self.view)




class SettingsView(discord.ui.View):
    def __init__(self, hatPremium: bool, userID: int):
        super().__init__(timeout=60)
        self.add_item(SettingSelect(hatPremium, userID))


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="settings", description="Change your Settings (like which sparks you can get)")
    async def settings(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        userID = str(interaction.user.id)
        premium = getPremium(connection, userID)
        locale = interaction.locale

        settingsObj = newSettings(premium, userID, locale)
        view = SettingsView(premium, userID)
        embed = settingsObj.getEmbed()
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)




async def setup(bot):
    await bot.add_cog(Settings(bot))
    print("SettingCommand geladen ✅")