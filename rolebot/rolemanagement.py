from redbot.core import commands
import discord
from discord.ext.commands.converter import ColorConverter

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, name: str, color: str = None, *perms: str):
        """Create a new role with the given name, color, and permissions.
        
        Example: !createrole "New Role" #FF5733 kick_members ban_members read_messages send_messages
        """
        guild = ctx.guild
        existing_role = discord.utils.get(guild.roles, name=name)
        if existing_role:
            await ctx.send(f"A role with the name '{name}' already exists.")
            return

        # Convert color from hex string to discord.Color
        try:
            if color:
                color = await ColorConverter().convert(ctx, color)
            else:
                color = discord.Color.default()
        except commands.BadArgument:
            await ctx.send("Invalid color format. Use a hex color code like #FF5733.")
            return

        # Create a discord.Permissions object from the provided perms
        permissions = discord.Permissions.none()
        valid_permissions = [perm for perm in dir(discord.Permissions) if not perm.startswith('_')]

        for perm in perms:
            if perm in valid_permissions:
                setattr(permissions, perm, True)
            else:
                await ctx.send(f"Invalid permission: {perm}")
                return

        # Create the role
        new_role = await guild.create_role(name=name, color=color, permissions=permissions)
        await ctx.send(f"Role '{new_role.name}' has been created with color {color} and permissions {', '.join(perms)}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def deleterole(self, ctx, *, name: str):
        """Delete a role with the given name."""
        guild = ctx.guild
        role_to_delete = discord.utils.get(guild.roles, name=name)
        if not role_to_delete:
            await ctx.send(f"No role with the name '{name}' found.")
        else:
            await role_to_delete.delete()
            await ctx.send(f"Role '{name}' has been deleted.")

    @commands.command()
    @commands.guild_only()
    async def listroles(self, ctx):
        """List all roles in the server."""
        roles = ctx.guild.roles
        role_names = [role.name for role in roles]
        await ctx.send(f"Roles in this server: {', '.join(role_names)}")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def addperm(self, ctx, role: discord.Role, *perms: str):
        """Add permissions to a role.
        
        Example: !addperm "Role Name" kick_members ban_members read_messages send_messages
        """
        permissions = role.permissions
        valid_permissions = [perm for perm in dir(discord.Permissions) if not perm.startswith('_')]

        for perm in perms:
            if perm in valid_permissions:
                setattr(permissions, perm, True)
            else:
                await ctx.send(f"Invalid permission: {perm}")
                return

        await role.edit(permissions=permissions)
        await ctx.send(f"Permissions {', '.join(perms)} have been added to the role '{role.name}'.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def removeperm(self, ctx, role: discord.Role, *perms: str):
        """Remove permissions from a role.
        
        Example: !removeperm "Role Name" kick_members ban_members read_messages send_messages
        """
        permissions = role.permissions
        valid_permissions = [perm for perm in dir(discord.Permissions) if not perm.startswith('_')]

        for perm in perms:
            if perm in valid_permissions:
                setattr(permissions, perm, False)
            else:
                await ctx.send(f"Invalid permission: {perm}")
                return

        await role.edit(permissions=permissions)
        await ctx.send(f"Permissions {', '.join(perms)} have been removed from the role '{role.name}'.")

def setup(bot):
    bot.add_cog(RoleManagement(bot))
