import re
from astrbot.api import star, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.core.message.components import Plain

# Comprehensive Unicode emoji regex covering all major emoji code blocks.
# Each range targets a specific Unicode emoji block to avoid matching
# non-emoji characters (e.g. CJK ideographs).
_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"   # Emoticons (😀-🙏)
    "\U0001F300-\U0001F5FF"   # Misc Symbols & Pictographs (🌀-🗿)
    "\U0001F680-\U0001F6FF"   # Transport & Map Symbols (🚀-🛿)
    "\U0001F1E0-\U0001F1FF"   # Regional Indicator Symbols / Flags
    "\U00002702-\U000027B0"   # Dingbats (✂-➰)
    "\U0001F900-\U0001F9FF"   # Supplemental Symbols & Pictographs (🤀-🧿)
    "\U0001FA00-\U0001FA6F"   # Chess Symbols (🨀-🩯)
    "\U0001FA70-\U0001FAFF"   # Symbols & Pictographs Extended-A (🩰-🫿)
    "\U00002600-\U000026FF"   # Miscellaneous Symbols (☀-⛿)
    "\U0000FE00-\U0000FE0F"   # Variation Selectors (VS1-VS16)
    "\U0000200D"              # Zero Width Joiner (ZWJ)
    "\U0000231A-\U0000231B"   # Watch ⌚, Hourglass ⌛
    "\U000023E9-\U000023F3"   # ⏩-⏳
    "\U000023F8-\U000023FA"   # ⏸-⏺
    "\U000023CF"              # ⏏ Eject
    "\U000025AA-\U000025AB"   # ▪-▫
    "\U000025B6"              # ▶ Play
    "\U000025C0"              # ◀ Reverse
    "\U000025FB-\U000025FE"   # ◻-◾
    "\U00002934-\U00002935"   # ⤴-⤵
    "\U00002B05-\U00002B07"   # ⬅-⬇
    "\U00002B1B-\U00002B1C"   # ⬛-⬜
    "\U00002B50"              # ⭐ Star
    "\U00002B55"              # ⭕ Hollow Red Circle
    "\U00003030"              # 〰 Wavy Dash
    "\U0000303D"              # 〽 Part Alternation Mark
    "\U00003297"              # ㊗ Circled Ideograph Congratulation
    "\U00003299"              # ㊙ Circled Ideograph Secret
    "\U000024C2"              # Ⓜ Circled Latin M
    "\U0001F004"             # 🀄 Mahjong Tile Red Dragon
    "\U0001F0CF"             # 🃏 Playing Card Black Joker
    "\U0001F18E"             # 🆎 AB Button
    "\U0001F191-\U0001F19A"  # 🆑-🆚 Squared Symbols
    "\U0001F200-\U0001F202"  # 🈀-🈂
    "\U0001F210-\U0001F23B"  # 🈐-🈻
    "\U0001F240-\U0001F248"  # 🉀-🉈
    "\U0001F250-\U0001F251"  # 🉐-🉑
    "]+",
    flags=re.UNICODE,
)


class Main(star.Star):
    def __init__(self, context: star.Context) -> None:
        super().__init__(context)

    @filter.on_decorating_result
    async def strip_emoji(self, event: AstrMessageEvent) -> None:
        """Strip all emoji characters from bot reply message chain before sending."""
        result = event.get_result()
        if result is None or not result.chain:
            return

        new_chain = []
        modified = False
        for comp in result.chain:
            if isinstance(comp, Plain):
                original = comp.text
                cleaned = _EMOJI_PATTERN.sub("", original)
                if cleaned != original:
                    modified = True
                    if cleaned:  # keep non-empty text only
                        new_chain.append(Plain(text=cleaned))
                else:
                    new_chain.append(comp)
            else:
                new_chain.append(comp)

        if modified:
            result.chain = new_chain
            logger.debug("[emoji_filter] Stripped emoji from outgoing message.")