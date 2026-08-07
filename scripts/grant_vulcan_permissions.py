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
            
    print(f"Updating permissions on server: {guild.name}")
    
    # 1. Find Vulcan role (case-insensitive)
    vulcan_role = None
    for r in guild.roles:
        if "vulcan" in r.name.lower():
            vulcan_role = r
            print(f"Found Vulcan role: {r.name} (ID: {r.id})")
            break
            
    if not vulcan_role:
        print("Error: Vulcan role not found. Please ensure you have invited the Vulcan bot to your server first.")
        await client.close()
        return
        
    # 2. Find channels
    verify_channel = discord.utils.get(guild.text_channels, name="holder-verify")
    mod_channel = discord.utils.get(guild.text_channels, name="mod-chat")
    
    # 3. Add Permission Overwrites for Vulcan in public verify channel
    if verify_channel:
        overwrite = verify_channel.overwrites_for(vulcan_role)
        overwrite.read_messages = True
        overwrite.send_messages = True
        overwrite.embed_links = True
        overwrite.attach_files = True
        await verify_channel.set_permissions(vulcan_role, overwrite=overwrite)
        print(f"Successfully granted Vulcan permissions in #{verify_channel.name}!")
    else:
        print("Warning: holder-verify channel not found.")
        
    # 4. Add Permission Overwrites for Vulcan in private mod-chat channel
    if mod_channel:
        overwrite = mod_channel.overwrites_for(vulcan_role)
        overwrite.read_messages = True
        overwrite.send_messages = True
        overwrite.embed_links = True
        overwrite.attach_files = True
        await mod_channel.set_permissions(vulcan_role, overwrite=overwrite)
        print(f"Successfully granted Vulcan permissions in #{mod_channel.name}!")
    else:
        print("Warning: mod-chat channel not found.")
    
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
