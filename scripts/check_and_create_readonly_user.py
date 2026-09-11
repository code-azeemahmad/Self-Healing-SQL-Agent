import asyncio
from app.db.engine import AsyncSessionLocal
from sqlalchemy import text


async def main():
    async with AsyncSessionLocal() as session:
        res = await session.execute(
            text("SELECT rolname FROM pg_roles WHERE rolname = 'shda_readonly'")
        )
        roles = res.scalars().all()
        print("Existing roles matching 'shda_readonly':", roles)

        if not roles:
            print("Creating role shda_readonly...")
            await session.execute(
                text("CREATE USER shda_readonly WITH PASSWORD 'shda_readonly_password'")
            )
            await session.execute(
                text("GRANT CONNECT ON DATABASE shda TO shda_readonly")
            )
            await session.execute(
                text("GRANT USAGE ON SCHEMA public TO shda_readonly")
            )
            await session.execute(
                text("GRANT SELECT ON ALL TABLES IN SCHEMA public TO shda_readonly")
            )
            await session.execute(
                text("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO shda_readonly")
            )
            await session.commit()
            print("shda_readonly role created and granted SELECT successfully!")
        else:
            print("Ensuring grants on tables...")
            await session.execute(
                text("GRANT CONNECT ON DATABASE shda TO shda_readonly")
            )
            await session.execute(
                text("GRANT USAGE ON SCHEMA public TO shda_readonly")
            )
            await session.execute(
                text("GRANT SELECT ON ALL TABLES IN SCHEMA public TO shda_readonly")
            )
            await session.execute(
                text("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO shda_readonly")
            )
            await session.commit()
            print("Permissions confirmed.")


if __name__ == "__main__":
    asyncio.run(main())
