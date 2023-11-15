from pyrubrum import transform

import anonyabbot


class Tree:
    @property
    def tree(self: "anonyabbot.FatherBot"):
        M = self._menu
        L = self._link
        P = self._page
        K = self._keyboard
        menu = {
            M("_chat_instruction"): {M("chat_instruction_confirm", "✅ 我已经仔细阅读并接受发言规则. ")},
            M("start"): {
                M("leave_group_confirm", "⏏️ 离开群组"): {M("leave_group", "⚠️ 是的, 我确定. ")},
                M("manage_group", "⚒️ 管理群组"): None,
                M("close_start", "❌ 关闭"): None,
            },
            M("_group_details"): {
                M("group_info", "ℹ️ 群组信息"): None,
                M("edit_group_profile", "⚒️ 群组资料", "ℹ️ 群组头像和简介只能在 @botfather 中编辑"): {
                    L("botfather_group", "转到 @botfather", url="t.me/botfather")
                },
                P(
                    "edit_default_ban_group",
                    "👑 成员默认权限",
                    "👤 成员默认权限:\n",
                    extras="_edbg_done",
                    per_page=8,
                ): {M("edbg_select")},
                M("edit_welcome_message", "⭐ 欢迎消息"): {
                    M("edit_welcome_message_message", "🧾 编辑消息"),
                    M("edit_welcome_message_button", "⌨️ 编辑按钮"),
                },
                M("edit_chat_instruction", "🧾 发言规则"): None,
                P("list_group_members", "👤 成员列表", extras=["_lgm_switch_activity", "_lgm_switch_role"]): {M("jump_member_detail")},
                M("close_group_details", "❌ 关闭"): None,
            },
            M("_edbg_done"): None,
            M("_lgm_switch_activity"): None,
            M("_lgm_switch_role"): None,
            M("_member_detail", back="list_group_members"): {
                K("edit_member_role_select", "👑 修改角色", "👑 选择角色"): {M("edit_member_role")},
                P("edit_member_ban_group", "⚠️ 修改权限", extras="_edit_member_ban_group_select_time"): {M("embg_select")},
                M("kick_member_confirm", "🚫 移除成员"): {M("kick_member", "⚠️ 是的, 我确定. ")},
            },
            K("_edit_member_ban_group_select_time", display="ℹ️ 选择时间"): {
                M("embg_done"): None,
            },
            M("_ewmb_ok_confirm", display="❓ 这是否正确? "): {M("_ewmb_ok", "✅ 确认", back=False)},
        }

        return transform(menu)
