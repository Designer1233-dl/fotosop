from __future__ import annotations

from typing import Any, Callable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


_premium_button_icon: Callable[[str], str | None] | None = None
_fmt_amount: Callable[[float], str] | None = None
_bot_asset = "USDT"


def configure_ui(
    premium_button_icon: Callable[[str], str | None],
    fmt_amount: Callable[[float], str],
    bot_asset: str,
) -> None:
    global _premium_button_icon, _fmt_amount, _bot_asset
    _premium_button_icon = premium_button_icon
    _fmt_amount = fmt_amount
    _bot_asset = bot_asset


def _icon(slot: str) -> str | None:
    if _premium_button_icon is None:
        return None
    return _premium_button_icon(slot)


def _amount(value: float) -> str:
    if _fmt_amount is None:
        return str(value)
    return _fmt_amount(value)


def main_menu_keyboard(is_admin: bool, games_enabled: bool) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    first_row = []
    if games_enabled:
        first_row.append(KeyboardButton(text="Играть", icon_custom_emoji_id=_icon("play_button")))
    else:
        first_row.append(KeyboardButton(text="История", icon_custom_emoji_id=_icon("history_button")))
    first_row.append(KeyboardButton(text="Профиль", icon_custom_emoji_id=_icon("profile_button")))
    builder.row(*first_row)
    if is_admin:
        builder.row(KeyboardButton(text="Админ-панель", icon_custom_emoji_id=_icon("log")))
    return builder.as_markup(resize_keyboard=True)


def profile_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Пополнить", callback_data="profile:deposit", icon_custom_emoji_id=_icon("deposit_button"))
    builder.button(text="Вывести", callback_data="profile:withdraw", icon_custom_emoji_id=_icon("withdraw_button"))
    builder.button(text="Рефералы", callback_data="profile:referrals", icon_custom_emoji_id=_icon("refs_button"))
    builder.button(text="Статистика", callback_data="profile:stats", icon_custom_emoji_id=_icon("stats_title"))
    builder.button(text="История", callback_data="profile:history", icon_custom_emoji_id=_icon("history_button"))
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def referrals_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="profile:open", icon_custom_emoji_id=_icon("back_button"))
    builder.adjust(1)
    return builder.as_markup()


def history_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="profile:open", icon_custom_emoji_id=_icon("back_button"))
    builder.adjust(1)
    return builder.as_markup()


def force_sub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Проверить подписку", callback_data="sub:check", icon_custom_emoji_id=_icon("subscribe_button"))]
        ]
    )


def admin_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Создать чек", callback_data="admin:create_check", icon_custom_emoji_id=_icon("check"))
    builder.button(text="Список чеков", callback_data="admin:checks", icon_custom_emoji_id=_icon("check"))
    builder.button(text="Комиссия проекта", callback_data="admin:house_commission", icon_custom_emoji_id=_icon("log"))
    builder.button(text="Режим вывода", callback_data="admin:withdraw_mode", icon_custom_emoji_id=_icon("withdraw_button"))
    builder.button(text="Рассылка", callback_data="admin:broadcast", icon_custom_emoji_id=_icon("log"))
    builder.button(text="Топ рефов", callback_data="admin:refs_top", icon_custom_emoji_id=_icon("win"))
    builder.button(text="Мин. ставка комнаты", callback_data="admin:min_room", icon_custom_emoji_id=_icon("main_menu"))
    builder.button(text="Мин. ставка ставок", callback_data="admin:min_bet", icon_custom_emoji_id=_icon("bets_button"))
    builder.button(text="Мин. пополнение", callback_data="admin:min_deposit", icon_custom_emoji_id=_icon("deposit"))
    builder.button(text="Мин. вывод", callback_data="admin:min_withdraw", icon_custom_emoji_id=_icon("withdraw"))
    builder.button(text="Депозит для вывода", callback_data="admin:withdraw_required_deposit", icon_custom_emoji_id=_icon("deposit"))
    builder.button(text="Реф. процент", callback_data="admin:ref_percent", icon_custom_emoji_id=_icon("profile"))
    builder.button(text="Добавить админа", callback_data="admin:add_admin", icon_custom_emoji_id=_icon("log"))
    builder.button(text="Выдать баланс", callback_data="admin:add_balance", icon_custom_emoji_id=_icon("deposit"))
    builder.button(text="Снять баланс", callback_data="admin:take_balance", icon_custom_emoji_id=_icon("withdraw"))
    builder.button(text="Канал подписки", callback_data="admin:force_sub", icon_custom_emoji_id=_icon("log"))
    builder.button(text="Лог-чат", callback_data="admin:log_chat", icon_custom_emoji_id=_icon("log"))
    builder.button(text="Статистика", callback_data="admin:stats", icon_custom_emoji_id=_icon("log"))
    builder.adjust(1)
    return builder.as_markup()


def gift_check_link(token: str, bot_username: str) -> str:
    return f"https://t.me/{bot_username}?start=check_{token}"


def gift_check_admin_keyboard(token: str, bot_username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Открыть чек", url=gift_check_link(token, bot_username), icon_custom_emoji_id=_icon("check"))
    builder.button(text="Управление", callback_data=f"giftcheck:view:{token}", icon_custom_emoji_id=_icon("log"))
    builder.adjust(1)
    return builder.as_markup()


def gift_check_public_keyboard(token: str, bot_username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Активировать", url=gift_check_link(token, bot_username), icon_custom_emoji_id=_icon("check"))
    builder.adjust(1)
    return builder.as_markup()


def check_skip_keyboard(step: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Пропустить", callback_data=f"checkskip:{step}", icon_custom_emoji_id=_icon("refresh_button"))
    builder.adjust(1)
    return builder.as_markup()


def gift_check_manage_keyboard(token: str, bot_username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Открыть чек", url=gift_check_link(token, bot_username), icon_custom_emoji_id=_icon("check"))
    builder.button(text="Удалить", callback_data=f"giftcheck:delete:{token}", icon_custom_emoji_id=_icon("delete_button"))
    builder.button(text="Назад", callback_data="admin:checks", icon_custom_emoji_id=_icon("back_button"))
    builder.adjust(1)
    return builder.as_markup()


def gift_check_list_keyboard(checks: list[Any]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for gift_check in checks:
        status = "ON" if int(gift_check["is_active"]) and int(gift_check["activations_left"]) > 0 else "OFF"
        builder.button(
            text=(
                f"{status} {gift_check['token']} • "
                f"{_amount(float(gift_check['amount']))} {_bot_asset} • "
                f"{int(gift_check['activations_left'])}/{int(gift_check['activations_total'])}"
            ),
            callback_data=f"giftcheck:view:{gift_check['token']}",
            icon_custom_emoji_id=_icon("check"),
        )
    builder.button(text="Назад", callback_data="admin:open", icon_custom_emoji_id=_icon("back_button"))
    builder.adjust(1)
    return builder.as_markup()


def gift_check_subscription_keyboard(token: str, channels: list[str]) -> InlineKeyboardMarkup:
    buttons = []
    for index, channel in enumerate(channels, start=1):
        buttons.append([InlineKeyboardButton(text=f"Канал {index}", url=channel, icon_custom_emoji_id=_icon("subscribe_button"))])
    buttons.append([InlineKeyboardButton(text="Проверить", callback_data=f"giftcheck:retry:{token}", icon_custom_emoji_id=_icon("refresh_button"))])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def withdraw_mode_keyboard(auto_enabled: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if auto_enabled:
        builder.button(text="Отключить авто-вывод", callback_data="withdrawmode:toggle", icon_custom_emoji_id=_icon("auto_withdraw_off"))
    else:
        builder.button(text="Включить авто-вывод", callback_data="withdrawmode:toggle", icon_custom_emoji_id=_icon("auto_withdraw_on"))
    builder.button(text="Назад", callback_data="admin:open", icon_custom_emoji_id=_icon("back_button"))
    builder.adjust(1)
    return builder.as_markup()


def withdraw_request_keyboard(request_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Одобрить", callback_data=f"withdraw:approve:{request_id}", icon_custom_emoji_id=_icon("win"))
    builder.button(text="Отклонить", callback_data=f"withdraw:reject:{request_id}", icon_custom_emoji_id=_icon("delete_button"))
    builder.adjust(2)
    return builder.as_markup()
