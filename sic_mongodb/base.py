from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Optional, Any, Tuple, Set
from loguru import logger
import asyncio
from pydantic import BaseModel
from typing import Optional, TypeVar, Type, List
from bson import ObjectId
from pymongo import ReturnDocument

PYDANTICTYPE = TypeVar("PYDANTICTYPE", bound=BaseModel)



class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db_name_space: List[str] = []
    collections_name_space: List[Tuple[str, Set[str]]] = []

    @classmethod
    async def connect(cls, host: str, port: int, **kwargs: Any) -> AsyncIOMotorClient:
        cls.client = AsyncIOMotorClient(f"mongodb://{host}:{port}", **kwargs)
        return cls.client

    @classmethod
    async def disconnect(cls):
        if cls.client:
            cls.client.close()
            cls.client = None

    @classmethod
    async def add_db(cls, db_name: str):
        cls.db_name_space.append(db_name)

    @classmethod
    async def add_collection(cls, db_name: str, collection_name: str):
        for db, collections in cls.collections_name_space:
            if db == db_name:
                collections.add(collection_name)
                return
        cls.collections_name_space.append((db_name, {collection_name}))

    @classmethod
    async def init_db(cls):
        if not cls.client:
            logger.warning("Client is not connected. Call connect() first.")
        for db in cls.db_name_space:
            database = cls.client[db]
            for db_name, collections in cls.collections_name_space:
                if db_name == db:
                    for collection in collections:
                        await database.create_collection(collection, check_exists=False)

    @classmethod
    async def create_data(
        cls, 
        db: AsyncIOMotorClient, 
        data: PYDANTICTYPE,
        collection_name: str
    ) -> ObjectId:
        for db_name, collections in cls.collections_name_space:
            if collection_name in collections:
                collection = db[collection_name]
                result = await collection.insert_one(data.model_dump())
                return result.inserted_id

    @classmethod
    async def get_all(
        cls, 
        db: AsyncIOMotorClient,
        collection_name: str, 
        length: int
    ) -> List[dict]:
        for db_name, collections in cls.collections_name_space:
            if collection_name in collections:
                collection = db[collection_name]
                documents = await collection.find().to_list(length=length)
                return documents

    @classmethod
    async def get_by_field(
        cls, 
        db: AsyncIOMotorClient, 
        field: str, 
        value: str,
        collection_name: str
    ) -> Optional[dict]:
        for db_name, collections in cls.collections_name_space:
            if collection_name in collections:
                collection = db[collection_name]
                document = await collection.find_one({field: value})
                return document

    @classmethod
    async def update_by_field(
        cls, 
        db: AsyncIOMotorClient, 
        field: str, 
        value: str, 
        update: dict,  # Add this argument for the update operation
        collection_name: str
    ) -> Optional[dict]:
        for db_name, collections in cls.collections_name_space:
            if collection_name in collections:
                collection = db[collection_name]
                updated_document = await collection.find_one_and_update(
                    {field: value},
                    {"$set": update},  # Pass the update operation here
                    return_document=ReturnDocument.AFTER
                )
                return updated_document


    @classmethod
    async def delete_by_field(
        cls, 
        db: AsyncIOMotorClient, 
        field: str, 
        value: str,
        collection_name: str
    ) -> int:
        for db_name, collections in cls.collections_name_space:
            if collection_name in collections:
                collection = db[collection_name]
                result = await collection.delete_one({field: value})
                return result.deleted_count






