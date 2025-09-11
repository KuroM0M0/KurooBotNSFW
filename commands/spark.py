import discord
import json
from discord.ext import commands
from discord import app_commands

with open("sparks.json", "r", encoding="utf8") as f:
    sparks_data = json.load(f)

art_choices = [
    app_commands.Choice(name="Soft", value="Soft"),
    app_commands.Choice(name="Spicy", value="Spicy"),
    app_commands.Choice(name="Explicit", value="Explicit")
]

class Spark(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="sparknsfw", description="Sende anonyme Sparks")
    @app_commands.describe(art="Wähle die Art des Sparks")
    @app_commands.choices(art=art_choices)
    async def sparkNSFW(self, interaction: discord.Interaction, art: str):
        await interaction.response.defer(ephemeral=True)

        # Filter die JSON nach dem gewählten Typ
        sparks_filtered_by_type = [
            (spark_key, spark_entry)
            for spark_key, spark_entry in sparks_data.items()
            if spark_entry["Typ"] == art
        ]

        # Erstelle Optionen für das Dropdown
        spark_options = [
            discord.SelectOption(label=spark_entry["name"], value=spark_key)
            for spark_key, spark_entry in sparks_filtered_by_type
        ]

        # Discord UI Select erstellen
        class SparkSelect(discord.ui.Select):
            def __init__(self):
                super().__init__(
                    placeholder="Wähle dein Spark",
                    min_values=1,
                    max_values=1,
                    options=spark_options
                )

            async def callback(self, interaction: discord.Interaction):
                selected_key = self.values[0]
                selected_spark = sparks_data[selected_key]
                await interaction.response.send_message(
                    f"{selected_spark['name']} {selected_spark['text']}", ephemeral=True
                )

        view = discord.ui.View()
        view.add_item(SparkSelect())
        await interaction.followup.send(
            "Wähle deinen Spark:", view=view, ephemeral=True
        )







# Setup-Funktion für Cog
async def setup(bot):
    await bot.add_cog(Spark(bot))
    print("SparkCommand geladen ✅")