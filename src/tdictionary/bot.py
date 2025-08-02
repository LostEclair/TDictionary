"""
This module contains an implementation of Telegram bot.
"""

from .env_config import TELEGRAM_BOT_TOKEN
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InputTextMessageContent, InlineQueryResultArticle
from logging import getLogger

from .search import search_limited_terms

logger = getLogger(__name__)
dp = Dispatcher()

ANSWER_TEMPLATE = """\
<b>{term}</b> <i>{additional}</i>
<i>{meaning}</i>

Синонимы: {synonims}

Смотрите также: {related_terms}"""


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        html.bold(
            "ккккороче!! cмотри, берешь, "
            "вызываешь меня через собачку, "
            "пишешь че надо, и усе ахеуть!"
        )
    )


@dp.inline_query()
async def inline_term_search(inline_query) -> None:
    if not (query := inline_query.query.strip()):
        return

    terms = await search_limited_terms(query)
    logger.info("%s has resulted %d results", query, len(terms))

    results = []
    for term in terms:
        additional = term.additional or ""
        meaning = term.definition or "Нету определения"
        synonims = term.synonyms or "Нету синонимов"
        related_terms = (
            ", ".join(html.code(every_term.term) for every_term in term.related_terms)
            if term.related_terms
            else "Нету похожих терминов"
        )

        expanded_message = ANSWER_TEMPLATE.format(
            term=term.term,
            additional=additional,
            meaning=meaning,
            synonims=synonims,
            related_terms=related_terms,
        )

        results.append(
            InlineQueryResultArticle(
                id=str(term.id),
                title=term.term,
                description=meaning,
                input_message_content=InputTextMessageContent(
                    message_text=expanded_message
                ),
            )
        )

    await inline_query.answer(results)


async def run_bot() -> None:
    await dp.start_polling(
        Bot(
            token=TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
    )
