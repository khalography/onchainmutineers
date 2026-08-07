import discord
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1535008736706428938

intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    guild = client.get_guild(GUILD_ID)
    if not guild:
        if client.guilds:
            guild = client.guilds[0]
        else:
            print("Error: Guild not found.")
            await client.close()
            return
            
    print(f"Updating server: {guild.name}")
    
    # 1. Get Category: 🌊 THE SHIP (PUBLIC)
    category_name = "🌊 THE SHIP (PUBLIC)"
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        print(f"Error: Category '{category_name}' not found.")
        await client.close()
        return
        
    # 2. Check if plunder-feed already exists
    channel_name = "plunder-feed"
    channel = discord.utils.get(category.channels, name=channel_name)
    
    # 3. Find roles
    everyone = guild.default_role
    captain = discord.utils.get(guild.roles, name="Captain")
    first_mate = discord.utils.get(guild.roles, name="First Mate")
    
    vulcan_role = None
    for r in guild.roles:
        if "vulcan" in r.name.lower():
            vulcan_role = r
            print(f"Found Vulcan role: {r.name} (ID: {r.id})")
            break
            
    # 4. Set overwrites
    overwrites = {
        everyone: discord.PermissionOverwrite(read_messages=True, send_messages=False),
    }
    if captain:
        overwrites[captain] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
    if first_mate:
        overwrites[first_mate] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
    if vulcan_role:
        overwrites[vulcan_role] = discord.PermissionOverwrite(
            read_messages=True, 
            send_messages=True,
            embed_links=True,
            attach_files=True
        )
        
    # 5. Create or Update Channel
    category_clean = category_name.encode('ascii', 'ignore').decode('ascii').strip()
    if not channel:
        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )
        print(f"Successfully created channel #{channel_name} in category '{category_clean}'!")
    else:
        print(f"Channel #{channel_name} already exists. Updating permissions...")
        for role, overwrite in overwrites.items():
            await channel.set_permissions(role, overwrite=overwrite)
        print("Permissions successfully updated!")
        
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
