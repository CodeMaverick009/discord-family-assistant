import discord

def create_recipe_embed(data):

    embed = discord.Embed(
        title=f"🍳 {data.get('title', 'Recipe')}",
        description=data.get("summary", ""),
        color=discord.Color.gold()
    )

    return embed