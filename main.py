import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.message.components import Plain

_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002600-\U000026FF"
    "\U0000FE00-\U0000FE0F"
    "\U0000200D"
    "\U0000231A-\U0000231B"
    "\U000023E9-\U000023F3"
    "\U000023F8-\U000023FA"
    "\U000023CF"
    "\U000025AA-\U000025AB"
    "\U000025B6"
    "\U000025C0"
    "\U000025FB-\U000025FE"
    "\U00002934-\U00002935"
    "\U00002B05-\U00002B07"
    "\U00002B1B-\U00002B1C"
    "\U00002B50"
    "\U00002B55"
    "\U00003030"
    "\U0000303D"
    "\U00003297"
    "\U00003299"
    "\U000024C2"
    "\U0001F004"
    "\U0001F0CF"
    "\U0001F18E"
    "\U0001F191-\U0001F19A"
    "\U0001F200-\U0001F202"
    "\U0001F210-\U0001F23B"
    "\U0001F240-\U0001F248"
    "\U0001F250-\U0001F251"
    "]+",
    flags=re.UNICODE,
)


@register("emoji_filter", "Nya-Nya-Hoshino", "Strip emoji characters from bot replies by Unicode code point matching.", "1.0.0")
class EmojiFilter(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.emoji_filter_enabled = self.config.get("emoji_filter_enabled", True)
        logger.info(f"[emoji_filter] Plugin loaded. enabled={self.emoji_filter_enabled}")

    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent):
        logger.info("[emoji_filter] on_decorating_result triggered")

        if not self.emoji_filter_enabled:
            logger.info("[emoji_filter] Disabled, skipping.")
            return

        result = event.get_result()
        if result is None:
            logger.info("[emoji_filter] result is None, skipping.")
            return
        if not result.chain:
            logger.info("[emoji_filter] result.chain is empty, skipping.")
            return

        modified = False
        new_chain = []
        for comp in result.chain:
            if isinstance(comp, Plain):
                original = comp.text
                cleaned = _EMOJI_PATTERN.sub("", original)
                if cleaned != original:
                    modified = True
                    logger.info(f"[emoji_filter] Emoji stripped: {original!r} -> {cleaned!r}")
                    if cleaned.strip():
                        new_chain.append(Plain(text=cleaned))
                else:
                    new_chain.append(comp)
            else:
                new_chain.append(comp)

        if modified:
            result.chain = new_chain
            logger.info("[emoji_filter] Message chain updated.")