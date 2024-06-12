from redbot.core import commands, Config
import discord

class RolePingControl(commands.Cog):
    """A cog to control who can ping specific roles based on their roles."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.config.register_guild(control_roles={})

    @commands.guild_only()
    @commands.admin_or_permissions(manage_roles=True)
    @commands.group()
    async def pingcontrol(self, ctx):
        """Group command for ping control settings."""
        pass

    @pingcontrol.command()
    async def setcontrol(self, ctx, control_role: discord.Role, target_role: discord.Role):
        """Set a role that is allowed to ping another role."""
        async with self.config.guild(ctx.guild).control_roles() as control_roles:
            control_roles[str(target_role.id)] = control_role.id
            await ctx.send(f"Role {control_role.name} can now ping {target_role.name}.")

    @pingcontrol.command()
    async def removecontrol(self, ctx, *target_roles: discord.Role):
        """Remove the control restriction for one or more target roles."""
        async with self.config.guild(ctx.guild).control_roles() as control_roles:
            removed_roles = []
            not_found_roles = []
            for target_role in target_roles:
                if str(target_role.id) in control_roles:
                    del control_roles[str(target_role.id)]
                    removed_roles.append(target_role.name)
                else:
                    not_found_roles.append(target_role.name)

            if removed_roles:
                await ctx.send(f"Control restriction removed for: {', '.join(removed_roles)}.")
            if not_found_roles:
                await ctx.send(f"No control restriction found for: {', '.join(not_found_roles)}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild = message.guild
        if guild is None:
            return

        control_roles = await self.config.guild(guild).control_roles()
        mentioned_roles = message.role_mentions

        for target_role in mentioned_roles:
            if str(target_role.id) in control_roles:
                control_role_id = control_roles[str(target_role.id)]
                control_role = guild.get_role(control_role_id)
                
                if control_role not in message.author.roles:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, you are not allowed to ping {target_role.name}.", delete_after=5)
                    break

