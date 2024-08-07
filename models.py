# models.py
from sqlalchemy import Table, Column, Integer, String, Text
from database import metadata

books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("title", String(100)),
    Column("author", String(100)),
    Column("description", Text, nullable=True),
    Column("year", Integer),
)
