from vkbottle.framework.framework.branch.database_branch import DatabaseBranch

from src.database.models import UserState


class MySqlBranch(DatabaseBranch):
    async def get_user(self, uid: int):
        """This method should return a tuple of two strings: branch name of the user and context"""
        u = await UserState.get(uid=uid)
        return u.branch, u.context

    async def set_user(self, uid: int, branch: str, context: str):
        """This method should make user's state or update it if exists"""
        u = await UserState.get_or_none(uid=uid)
        if u is not None:
            u.branch = branch
            u.context = context
            return await u.save()
        await UserState.create(uid=uid, branch=branch, context=context)

    async def all_users(self):
        """This method should return user_ids of all stated users"""
        return [u.uid async for u in UserState.all()]

    async def delete_user(self, uid: int):
        """This method should delete the user's bot from the database"""
        u = await UserState.get(uid=uid)
        await u.delete()
