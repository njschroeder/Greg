import discord
from discord.ui import View, Modal, TextInput, UserSelect

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
        self.value = True
        self.stop()

    @discord.ui.button(label="Decline Duel?", style=discord.ButtonStyle.red, emoji="❎")
    async def decline_callback(self, interaction, button):
        for x in self.children:
            x.disabled = True
        await interaction.response.edit_message(view=self)
        self.value = False
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user.id != self.intended_user_id:
            await interaction.response.send_message(content="This is not for you :).", ephemeral=True)
            return False
        return True

# Select Menus for getting names and games
class Games(View):
    def __init__(self, sender_id):
        super().__init__()
        self.sender_id = sender_id

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Choose a game!",
        options=[
            discord.SelectOption(
                label="Tic Tac Toe",
                emoji="❌",
                description="Tic Tac Toe played using emojis."
            )
        ]
    )

    async def callback(self, interaction, select):
        select.disabled = True
        await interaction.response.edit_message(view=self)
        self.value = select.values[0]
        await interaction.followup.send(f"You chose {self.value}.", ephemeral=True)
        self.stop()
    
    async def interaction_check(self, interaction) -> bool:
        if interaction.user.id != self.sender_id:
            print(interaction.user.id, self.sender_id)
            await interaction.response.send_message(content="This is not for you :).", ephemeral=True)
            return False
        return True
    

# for selecting another member
class Names(View):
    def __init__(self, sender_id):
        super().__init__()
        self.sender_id = sender_id

    @discord.ui.select(
        cls=UserSelect,
        placeholder="Type or select a user's display name",
    )
    async def callback(self, interaction, select):
        self.value = select.values[0]
        select.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()
    
    async def interaction_check(self, interaction) -> bool:
        if interaction.user.id != self.sender_id:
            print(interaction.user.id, self.sender_id)
            await interaction.response.send_message(content="This is not for you :).", ephemeral=True)
            return False
        return True
