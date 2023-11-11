from textwrap import indent
from pyrogram import Client
from pyrogram.types import Message as TM, CallbackQuery as TC

import anonyabbot

from ...model import User, Group
from ...utils import remove_prefix, truncate_str
from ..pool import stop_group_bot
from .common import operation


class Start:
    @operation(prohibited=None)
    async def on_start(
        self: "anonyabbot.FatherBot",
        handler,
        client: Client,
        context: TM,
        parameters: dict,
    ):
        if isinstance(context, TM):
            if not context.text:
                return None
            cmds = context.text.split()
            if len(cmds) == 2:
                if cmds[1] == "_usecode":
                    return await self.to_menu("use_code", context)
                elif cmds[1].startswith("_g_"):
                    gid = remove_prefix(cmds[1], "_g_")
                    return await self.to_menu("_group_detail", context, gid=gid)
        return f"🌈 Welcome {context.from_user.name}!\n\n" "This bot allows you to create a completely anonymous group."

    @operation(prohibited=None)
    async def on_my_info(
        self: "anonyabbot.FatherBot",
        handler,
        client: Client,
        context: TC,
        parameters: dict,
    ):
        user: User = context.from_user.get_record()
        msg = (
            f"ℹ️ Profile of {user.name}:\n\n"
            f" ID: {user.uid}\n"
            f" Created Groups: {user.created_groups.count()}\n"
            f" Created: {user.created.strftime('%Y-%m-%d')}\n"
        )
        roles = [r.display for r in user.roles()]
        if roles:
            msg += f"\n👑 Roles:\n"
            for r in roles:
                msg += f"  - {r.title()}\n"
        return msg

    @operation()
    async def on_use_code(
        self: "anonyabbot.FatherBot",
        handler,
        client: Client,
        context: TC,
        parameters: dict,
    ):
        self.set_conversation(context, "use_code")
        return "❓ Type your code:"

    @operation()
    async def on_new_group(
        self: "anonyabbot.FatherBot",
        handler,
        client: Client,
        context: TC,
        parameters: dict,
    ):
        self.set_conversation(context, "ng_token")
        return (
            "🌈 Guide\n\n"
            "Your anonymous group will be a newly created bot (yes, bot).\n"
            "Any information sent by anyone to the bot will be forwarded to all users with their identity hidden.\n"
            "You need to create a new bot through @botfather and forward the message including bot token to me."
        )

    @operation()
    async def on_list_group(
        self: "anonyabbot.FatherBot",
        handler,
        client: Client,
        context: TC,
        parameters: dict,
    ):
        user: User = context.from_user.get_record()
        items = []
        g: Group
        for i, g in enumerate(user.groups(created=True)):
            item = f"{i+1} | [{truncate_str(g.title, 45)}](t.me/{g.username})"
            items.append((item, str(i + 1), g.id))
        if not items:
            await self.info("⚠️ No group available.", context=context)
            await self.to_menu("start", context)
        return items

    @operation()
    async def on_jump_group_detail(
        self: "anonyabbot.FatherBot",
        handler,
        client: Client,
        context: TC,
        parameters: dict,
    ):
        parameters["group_id"] = int(parameters["jump_group_detail_id"])
        await self.to_menu("_group_detail", context)

    @operation()
    async def on_group_detail(
        self: "anonyabbot.FatherBot",
        handler,
        client: Client,
        context: TC,
        parameters: dict,
    ):
        group: Group = Group.get_by_id(parameters["group_id"])
        msg = f"⭐ Group info for [@{group.username}](t.me/{group.username}):\n\n"
        fields = [
            f"Title: [{group.title}](t.me/{group.username})",
            f"Creator: {group.creator.markdown}",
            f"Members: {group.n_members}",
            f"Messages: {group.n_messages}",
            f"Disabled: {'**Yes**' if group.disabled else 'No'}",
            f"Created: {group.created.strftime('%Y-%m-%d')}",
            f"Last Activity: {group.last_activity.strftime('%Y-%m-%d')}",
        ]
        msg += indent("\n".join(fields), "  ")
        msg += "\n\n⬇️ Click the buttons below to configure the group:"
        return msg

    @operation()
    async def on_delete_group_confirm(
        self: "anonyabbot.FatherBot",
        handler,
        client: Client,
        context: TC,
        parameters: dict,
    ):
        group: Group = Group.get_by_id(parameters["group_id"])
        return (
            f"⚠️ Are you sure to delete the group [@{group.username}](t.me/{group.username})?\n"
            f"⚠️ This group has {group.n_members} members and {group.n_messages} messages.\n"
            f'⚠️ This group was created at {group.created.strftime("%Y-%m-%d")}.'
        )

    @operation()
    async def on_delete_group(
        self: "anonyabbot.FatherBot",
        handler,
        client: Client,
        context: TC,
        parameters: dict,
    ):
        group: Group = Group.get_by_id(parameters["group_id"])
        await stop_group_bot(group.token)
        group.disabled = True
        group.save()
        await context.answer("✅ Group deleted.")
        await self.to_menu("list_group", context)