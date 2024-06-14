from sqlalchemy.ext.asyncio import AsyncSession

class GeneralService():
    async def book_search(self, db: AsyncSession, query: str, max_results: int = 7):
        return None