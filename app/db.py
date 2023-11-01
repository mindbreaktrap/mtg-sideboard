from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


async def init():
    client = AsyncIOMotorClient(
        "mongodb://default_username_local_only:default_password_local_only@localhost:27017"
    )
    await init_beanie(
        database=client.mtgsideboards, document_models=["app.models.decklist.Decklist"]
    )
