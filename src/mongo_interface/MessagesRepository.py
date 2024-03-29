from typing import Any, Union

from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from src.mongo_interface.DBConnection import get_db_collections_mess
from src.models.MessangeClass import Messages, UpdateMessagesModel


def map_messages(mess: Any) -> Union[Messages, bool]:
    try:
        id = str(mess.get("_id", ""))
        PostTypeId = (mess.get("PostTypeId", 0))
        AcceptedAnswerId = (mess.get("AcceptedAnswerId", 0))
        CreationDate = (mess.get("CreationDate", '2040-01-12T15:45:19.963'))
        Score = (mess.get("Score", 0))
        ViewCount = (mess.get("ViewCount", 0))
        Body = (mess.get("Body", ''))
        OwnerUserId = (mess.get("OwnerUserId", 0))
        LastActivityDate = (
            mess.get(
                "LastActivityDate",
                '2040-01-12T15:45:19.963'))
        Title = (mess.get("Title", ''))
        Tags = (mess.get("Tags", ''))
        AnswerCount = (mess.get("AnswerCount", 0))
        CommentCount = (mess.get("CommentCount", 0))
        ContentLicense = (mess.get("ContentLicense", ''))
        LastEditorUserId = (mess.get("LastEditorUserId", ''))
        LastEditDate = (mess.get("LastEditDate", '2040-01-12T15:45:19.963'))
    except Exception as e:
        print(f"Error occurred while mapping messages: {e}")
        return False
    finally:
        return Messages(
            id=id,
            PostTypeId=PostTypeId,
            AcceptedAnswerId=AcceptedAnswerId,
            CreationDate=CreationDate,
            Score=Score,
            ViewCount=ViewCount,
            Body=Body,
            OwnerUserId=OwnerUserId,
            LastActivityDate=LastActivityDate,
            Title=Title,
            Tags=Tags,
            AnswerCount=AnswerCount,
            CommentCount=CommentCount,
            ContentLicense=ContentLicense,
            LastEditorUserId=LastEditorUserId,
            LastEditDate=LastEditDate)


def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}


class MessageRepository:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def find_all(self) -> list[Messages]:
        db_mess = []
        async for mes in self._db_collection.find():
            db_mess.append(map_messages(mes))
            print(mes)
        return db_mess

    async def create_post(self, mess: UpdateMessagesModel) -> str:
        insert_post = await self._db_collection.insert_one(dict(mess))
        return str(insert_post.inserted_id)

    async def update_post(self, mess_id: str, mess: UpdateMessagesModel) -> Any:
        db_post = await self._db_collection.find_one_and_replace(get_filter(mess_id), dict(mess))
        chech = map_messages(db_post)
        if not chech:
            return False
        return chech

    async def find_mess_by_id(self, mess_id: str) -> Any:
        db_post = await self._db_collection.find_one(get_filter(mess_id))

        return map_messages(db_post)

    async def find_paginated(self, page: int, page_size: int) -> list[Messages]:
        skip = (page - 1) * page_size
        db_mess = []
        async for mes in self._db_collection.find().skip(skip).limit(page_size):
            print(mes)
            db_mess.append(map_messages(mes))
        return db_mess

    async def count_documents(self, skip: int) -> list[Messages]:
        page_size = 15000
        db_mess = []
        total_documents = self._db_collection.count_documents({})
        total_pages = -(-int(total_documents) // page_size)
        async for mes in self._db_collection.find().skip(skip).limit(page_size):
            print(mes)
            db_mess.append(map_messages(mes))
        return db_mess

    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(
            get_db_collections_mess)):
        return MessageRepository(db_collection)
