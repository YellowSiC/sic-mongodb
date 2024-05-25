from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from loguru import logger
import asyncio
from pydantic import BaseModel
from typing import Optional,List
from bson import ObjectId
from .base import MongoDB, PYDANTICTYPE




async def insert(
    db: AsyncIOMotorClient, 
    data: PYDANTICTYPE,
    collection_name: str
    ) -> ObjectId:

    inserted_id = await MongoDB.create_data(
        db=db, 
        data=data, 
        collection_name=collection_name
        )
    return inserted_id

async def get_all(
    db: AsyncIOMotorClient,
    collection_name: str, 
    length: int
    ) -> List[dict]:
    inserted_id = await MongoDB.get_all(
        db=db, 
        collection_name=collection_name, 
        length=length
        )
    return inserted_id



async def get_single(
    db: AsyncIOMotorClient, 
    field: str, 
    value: str,
    collection_name: str
    ) -> Optional[dict]:

    inserted_id = await MongoDB.get_by_field(
        db=db, 
        field=field, 
        value=value, 
        collection_name=collection_name
        )
    return inserted_id


async def update_single(
    db: AsyncIOMotorClient, 
    field: str, 
    value: str, 
    update: dict,
    collection_name: str
    ) -> Optional[dict]:
    inserted_id = await MongoDB.update_by_field(
        db=db, 
        field=field, 
        value=value, 
        collection_name=collection_name, 
        update=update
        )
    return inserted_id


async def delete_single(
    db: AsyncIOMotorClient, 
    field: str, 
    value: str,
    collection_name: str
    ) -> int:
    inserted_id = await MongoDB.delete_by_field(
        db=db, 
        field=field, 
        value=value, 
        collection_name=collection_name
        )
    return inserted_id


async def create_db(database_name:str, collections:List[str]=[]):
    await MongoDB.add_db(database_name)
    for collection in collections:
        await MongoDB.add_collection(database_name, collection)

async def connect(host: str, port: int) -> AsyncIOMotorClient:
    logger.info("Connection in Progress")
    db = await MongoDB.connect(host, port)
    if db:
        logger.success("Connection Progress Successfully")
    else:
        logger.warning("Connection Progress failed")

    return db



async def init_db():
    db = await MongoDB.init_db()
    if db:
        logger.success("Initiald Successfully")
        return db
    else:
        logger.warning("Close failed")
    

async def get_session() -> AsyncIOMotorClient:
    if MongoDB.client is None:
        logger.warning("Database client is not connected. Call connect() first.")
    return MongoDB.client



async def close():
    db = await MongoDB.disconnect()
    if db:
        logger.success("Closed Successfully")
    else:
        logger.warning("Close failed")