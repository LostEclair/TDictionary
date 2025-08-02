"""
This module contains SQLAlchemy models, engine and init function.
"""

from logging import getLogger

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, backref, relationship
from sqlalchemy.schema import UniqueConstraint

from .env_config import DATABASE_URL

logger = getLogger(__name__)
sql_engine = create_async_engine(DATABASE_URL)


class Base(DeclarativeBase): ...


class AssocTermsTerms(Base):
    __tablename__ = "assoc_terms_terms"
    __table_args__ = (UniqueConstraint("term_id", "related_id", name="uq_term_relation"),)

    term_id = Column(Integer, ForeignKey("terms.id"), primary_key=True)
    related_id = Column(Integer, ForeignKey("terms.id"), primary_key=True)


class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True)
    term = Column(String, nullable=False, unique=True)
    additional = Column(String)
    definition = Column(String)
    synonyms = Column(String)
    origin = Column(String)
    example_text = Column(String)

    related_terms = relationship(
        "Term",
        secondary="assoc_terms_terms",
        primaryjoin=(id == AssocTermsTerms.term_id),
        secondaryjoin=(id == AssocTermsTerms.related_id),
        backref=backref("related_by", lazy="dynamic"),
        lazy="selectin",
    )


async def initialize_database() -> None:
    logger.info("Initializing database")
    async with sql_engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
        except Exception as ectx:
            logger.exception(
                "An error occured during database initialization: %s",
                ectx,
                exc_info=True,
            )
