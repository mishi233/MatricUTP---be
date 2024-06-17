from sqlalchemy.ext.asyncio import AsyncSession

class GeneralService():

    @staticmethod
    async def initialize_db(db: AsyncSession):
        """
            Inicializar datos primordiales para el funcionamiento del software.
        """    

    async def book_search(self, db: AsyncSession):
        return None