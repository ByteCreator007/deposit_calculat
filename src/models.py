from sqlalchemy import Table, Column, Integer, Float, MetaData, Text, Date

metadata = MetaData()

deposits = Table(
    "deposits",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", Date, nullable=False),
    Column("periods", Integer, nullable=False),
    Column("amount", Float, nullable=False),
    Column("rate", Float, nullable=False),
    Column("result", Text, nullable=False),
)
