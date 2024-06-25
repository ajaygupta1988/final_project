import motor.motor_asyncio
from components import Utils
from datetime import datetime, timedelta
from schemas import ExternalResponseDataSchema, DataSchema, MetaDataSchema
from config import settings


class QueryManager:
    def __init__(self, client=None) -> None:
        # mongo database instance
        self.mongo_client = client or motor.motor_asyncio.AsyncIOMotorClient(
            settings.database_url,
            tls=settings.database_tls,
            tlsAllowInvalidCertificates=True,
        )
        self.database = self.mongo_client[settings.database]
        self.data_collection = self.database.get_collection("data_collection")
        self.meta_data_collection = self.database.get_collection("meta_data_collection")

    async def add_data_from_api(self, data: ExternalResponseDataSchema):
        data_to_insert = Utils().standardize_external_data(data)
        data_insert = await self.data_collection.insert_many(data_to_insert)
        meta_data_insert = await self.meta_data_collection.insert_one(
            data.meta_data.model_dump()
        )
        return {"detail": "data successfully inserted"}

    async def check_if_data_is_missing_or_stale(
        self, symbol: str, stale_duration_days: int = 10
    ):
        meta_data_record = await self.meta_data_collection.find_one({"symbol": symbol})
        # If meta_data_record is null, return True indicating missing data
        if not meta_data_record:
            return True
        # Get the last_refreshed date from the meta data record
        last_refreshed_date = meta_data_record.get("last_refresh")

        # Calculate the threshold date for stale data
        threshold_date = datetime.now() - timedelta(days=stale_duration_days)

        # Check if last_refreshed is older than this week
        if last_refreshed_date < threshold_date:
            delete_data = await self.data_collection.delete_many({"symbol": symbol})
            return True  # Data is stale

        else:
            return False  # Data is not stale

    async def get_symbol_data(self, symbol: str) -> list[DataSchema]:
        result = []
        cursor = self.data_collection.find({"symbol": symbol})
        async for document in cursor:
            document["_id"] = str(document["_id"])
            result.append(document)
        return result

    async def get_available_symbols(self) -> list[MetaDataSchema]:
        result = []
        cursor = self.meta_data_collection.find()
        async for document in cursor:
            document["_id"] = str(document["_id"])
            result.append(document)

        return result
