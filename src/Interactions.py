import discord
from discord.ui import View, Button

# for duel interaction
class Duel(View):
    def __init__(self, intended_user_id):
        super().__init__()
        self.intended_user_id = intended_user_id
        self.value = None
    
    @discord.ui.button(label="Accept Duel?", style=discord.ButtonStyle.green, emoji="⚔️")
    async def accept_callback(self, interaction, button):
        for x in self.children:
            x.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"You Accepted!", ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label="Decline Duel?", style=discord.ButtonStyle.red, emoji="❎")
    async def decline_callback(self, interaction, button):
        for x in self.children:
            x.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"You Declined!", ephemeral=True)
        self.value = False
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user.id != self.intended_user_id:
            await interaction.response.send_message(content="This is not for you :).", ephemeral=True)
            return False
        return True

