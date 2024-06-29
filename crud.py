import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User, Profile, Post
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedLoad, selectinLoad

async def create_user(session: AsyncSession, username: str) -> None:
    user = User(username=username)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one()
    return user


async def create_user_profile(session: AsyncSession, user_id: int, first_name: str | None) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> list[User]:
    stmt = select(User).options(joinedLoad(User.profile)).order_by(User.id)
    await session.scalars(stmt)


async def create_posts(session: AsyncSession, user_id: int, *posts_titles: str) -> list[Post]:
    posts = [
        Post(title=title, user_id=user_id)
        for title in posts_titles
    ]
    session.add_all(posts)
    await session.commit()
    return posts


async def get_users_with_posts(
        session: AsyncSession,
):
    stmt = select(User).options(selectinLoad(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedLoad(Post.user), selectinLoad(User.posts)).order_by(Post.id)
    posts = await session.scalars(stmt)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedLoad(Profile.user).selectinLoad(User.posts),
        )
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)


async def main():
    async with db_helper.session_factory() as session:
        await create_user(session=session, username="john")
        await get_user_by_username(session=session, username="sam")
        user_john = await get_user_by_username(session=session, username="john")
        await create_user_profile(
            session=session,
            user_id=user_john.id,
            first_name="John",
        )
        await get_users_with_posts(session=session)
        await get_posts_with_authors(session=session)


if __name__ == '__main__':
    asyncio.run(main())
