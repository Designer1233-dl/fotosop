from __future__ import annotations

import re
from typing import Any

from aiogram import Bot
from aiogram.types import Message


PREMIUM_EMOJI_IDS = {
    "main_menu": "5325547803936572038",
    "profile": "5390998591516977527",
    "check": "5197434882321567830",
    "win": "5260616239247563540",
    "lose": "5260258807774218256",
    "deposit": "5201691993775818138",
    "withdraw": "5312123810638483121",
    "log": "5267014542222723292",
    "play_button": "5267014542222723292",
    "profile_button": "5258204546391351475",
    "create_room_button": "5472427031100667803",
    "rooms_button": "5386367538735104399",
    "my_rooms_button": "5316727448644103237",
    "deposit_button": "5258336354642697821",
    "withdraw_button": "5260379144167890225",
    "refs_button": "5258486128742244085",
    "back_button": "5258236805890710909",
    "refresh_button": "5258420634785947640",
    "delete_button": "5210952531676504517",
    "subscribe_button": "5258073068852485953",
    "profile_balance": "5197434882321567830",
    "profile_ref_income": "5330320040883411678",
    "profile_ref_count": "5217822164362739968",
    "game_menu_title": "5399909394525737759",
    "bets_button": "5890971177484029249",
    "bet_product_button": "5890934648787176897",
    "bet_odd_button": "5890934648787176897",
    "bet_even_button": "5890934648787176897",
    "bet_sixty_five_button": "5890934648787176897",
    "dice_button": "5890934648787176897",
    "stats_title": "5230974475209554508",
    "stats_deposit": "5472427031100667803",
    "stats_withdraw": "5230974475209554508",
    "stats_result": "5271912827869737544",
    "history_title": "5230974475209554508",
    "history_button": "5258420634785947640",
    "history_entry": "5267014542222723292",
    "auto_withdraw_menu": "5260379144167890225",
    "auto_withdraw_on": "5260616239247563540",
    "auto_withdraw_off": "5210952531676504517",
    "games_off": "",
}
PREMIUM_TEXT_EMOJI_SLOTS = {
    "вњЁ": "main_menu",
    "рџ”Ґ": "main_menu",
    "рџЋ°": "main_menu",
    "вћ•": "main_menu",
    "рџ‘¤": "profile",
    "рџ‘®": "profile",
    "рџЋЃ": "profile_ref_income",
    "рџ‘Ґ": "profile_ref_count",
    "рџ’°": "profile_balance",
    "рџЏ†": "win",
    "вњ…": "win",
    "рџ‘‘": "win",
    "рџ¤ќ": "win",
    "вќЊ": "lose",
    "рџљЁ": "lose",
    "рџ’і": "deposit",
    "рџ’µ": "deposit",
    "рџ’ё": "withdraw",
    "вљ™пёЏ": "log",
    "вљ пёЏ": "log",
    "рџ’ј": "log",
    "рџ›Ў": "log",
    "рџ§ѕ": "log",
    "рџ“ќ": "log",
    "рџ–ј": "log",
    "рџ”—": "log",
    "рџ“Ј": "log",
    "рџ“Љ": "log",
    "рџ“Ќ": "log",
    "рџ—‚": "log",
    "рџ“‹": "rooms_button",
    "рџ“Ў": "subscribe_button",
    "рџ”’": "subscribe_button",
    "рџ”ђ": "subscribe_button",
    "рџ”“": "subscribe_button",
    "рџЋџ": "check",
    "рџ”‘": "check",
    "рџ—‘": "delete_button",
    "рџ”Ѓ": "refresh_button",
    "рџЋІ": "game_menu_title",
    "рџ•’": "history_title",
    "рџ“њ": "history_entry",
}
TG_EMOJI_TAG_RE = re.compile(r"<tg-emoji\b[^>]*>.*?</tg-emoji>", re.DOTALL)

_ORIGINAL_MESSAGE_ANSWER = Message.answer
_ORIGINAL_MESSAGE_EDIT_TEXT = Message.edit_text
_ORIGINAL_BOT_SEND_MESSAGE = Bot.send_message
_ORIGINAL_BOT_SEND_PHOTO = Bot.send_photo
_HOOKS_INSTALLED = False


def premium_emoji(slot: str, fallback: str) -> str:
    emoji_id = PREMIUM_EMOJI_IDS.get(slot)
    if not emoji_id:
        return fallback
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'


def premium_button_icon(slot: str) -> str | None:
    emoji_id = PREMIUM_EMOJI_IDS.get(slot)
    return emoji_id or None


def premiumize_text(text: str | None) -> str | None:
    if not text:
        return text

    protected_tags: list[str] = []

    def protect_tag(match: re.Match[str]) -> str:
        protected_tags.append(match.group(0))
        return f"__TG_EMOJI_TAG_{len(protected_tags) - 1}__"

    result = TG_EMOJI_TAG_RE.sub(protect_tag, text)
    for emoji, slot in sorted(PREMIUM_TEXT_EMOJI_SLOTS.items(), key=lambda item: len(item[0]), reverse=True):
        result = result.replace(emoji, premium_emoji(slot, emoji))
    for index, tag in enumerate(protected_tags):
        result = result.replace(f"__TG_EMOJI_TAG_{index}__", tag)
    return result


async def _premium_message_answer(self: Message, text: str, *args, **kwargs):
    return await _ORIGINAL_MESSAGE_ANSWER(self, premiumize_text(text), *args, **kwargs)


async def _premium_message_edit_text(self: Message, text: str, *args, **kwargs):
    return await _ORIGINAL_MESSAGE_EDIT_TEXT(self, premiumize_text(text), *args, **kwargs)


async def _premium_bot_send_message(self: Bot, chat_id: int | str, text: str, *args, **kwargs):
    return await _ORIGINAL_BOT_SEND_MESSAGE(self, chat_id, premiumize_text(text), *args, **kwargs)


async def _premium_bot_send_photo(self: Bot, chat_id: int | str, photo: Any, *args, **kwargs):
    caption = kwargs.get("caption")
    if isinstance(caption, str):
        kwargs["caption"] = premiumize_text(caption)
    return await _ORIGINAL_BOT_SEND_PHOTO(self, chat_id, photo, *args, **kwargs)


def install_premium_hooks() -> None:
    global _HOOKS_INSTALLED
    if _HOOKS_INSTALLED:
        return
    Message.answer = _premium_message_answer
    Message.edit_text = _premium_message_edit_text
    Bot.send_message = _premium_bot_send_message
    Bot.send_photo = _premium_bot_send_photo
    _HOOKS_INSTALLED = True
