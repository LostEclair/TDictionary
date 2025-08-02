"""
This module implements search function for tdictionary.database.Term
"""

from logging import getLogger
from .database import sql_engine, Term
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload
from sqlalchemy import select

logger = getLogger(__name__)

local_session = async_sessionmaker(
    bind=sql_engine, expire_on_commit=False, class_=AsyncSession
)


async def search_limited_terms(query: str, limit: int = 16) -> list[Term]:
    try:
        async with local_session() as session:
            search_results = await session.execute(
                select(Term)
                .options(selectinload(Term.related_terms))
                .where(Term.term.ilike(f"{query}%"))
                .order_by(Term.term)
                .limit(limit)
            )

            return list(search_results.scalars())
    except Exception as ectx:
        logger.error("Error searching terms for '%s': %s", query, ectx, exc_info=True)
        return []
