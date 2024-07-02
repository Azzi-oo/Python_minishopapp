import asyncio
from api_v1.products.schemas import Product
from core.models.order import Order
from core.models.order_product_association import OrderProductAssociation
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


async def create_order(session: AsyncSession, promocode: str | None  = None) -> Order:
    order = Order(promocode=promocode)

    session.add(order)
    await session.commit()
    return order


async def create_product(
        session: AsyncSession,
        name: str,
        price: int,
        description: str,
) -> Product:
    product = Product(
        name=name,
        description=description,
        price=price,
    )
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    orders = await get_orders_with_products(session)


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinLoad(Order.products),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)

    return list[orders]


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)


async def get_orders_with_products_assoc(session: AsyncSession):
    stmt = (
        select(Order)
        .options(
            selectinLoad(Order.products_details).joinedLoad(OrderProductAssociation.product),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)

    return list(orders)


async def main_relations(session: AsyncSession):
    async with db_helper.session_factory() as session:
        await main_relations(session)
        await demo_m2m(session)


async def demo_m2m(session: AsyncSession):
    order = await create_order(session)
    order_promo = await create_order(session, promocode="promo")

    mouse = await create_product(session, "Mouse", "Description gaming mouse", price=123,)
    keyboard = await create_product(session, "Keyboard", "Great gaming keyboard", price=149,)

    order = await session.scalar(select(Order).where(Order.id == order.id), options=(selectinLoad(Order.products),),)
    order_promo = await session.scalar(select(Order).where(Order.id == order_promo.id), options=(selectinLoad(Order.products),),)
    order.products.append(mouse)
    order.products.append(keyboard)
    order_promo.products.append(mouse)
    order_promo.products.append(keyboard)

    order_promo.products = [keyboard]

    await session.commit()


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
