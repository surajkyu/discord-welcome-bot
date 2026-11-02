import asyncio
import asyncpg

# Use for local database

async def create_pool():
    pool = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="welcome_bot", # welcome_bot user
        password="wbot", # password for welcome_bot user
        database="welcome_bot" # database name
    )

    return pool

# create pool powered by neon.tech for hosting
# async def create_pool():
#     return await asyncpg.create_pool(
#         os.getenv("DATABASE_URL")
#     )
#
#     return pool
#
