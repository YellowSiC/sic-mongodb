


## 📦 Install

```bash

pip install pymongo 
pip install motor
pip install loguru
pip install pydantic      

```


## Usage

```python

from loguru import logger
from pydantic import BaseModel
from sic_mongodb import (
    connect,
    init_db,
    get_session,
    create_db,
    insert,
    get_all,
    get_single,
    update_single,
    delete_single,
    close
    
)
import asyncio



class SampleData(BaseModel):
    name: str
    age: int




async def main():
    # Connect to MongoDB
    await connect('localhost', 27017)
    
    # Add database and collection
    await create_db('test_db_1', collections=["test_collection", "test_collection_1", "test_collection_2"])
    # Initialize database
    await init_db()

    # Get database session
    db = await get_session()

    # Create data
    sample_data = SampleData(name="John Doe", age=30)
    inserted_id = await insert(db['test_db_1'], sample_data, collection_name='test_collection')
    logger.info(f"Inserted ID: {inserted_id}")

    # Retrieve all data
    all_data = await get_all(db['test_db_1'], 'test_collection', 10)
    logger.info(f"All Data: {all_data}")

    # Retrieve data by field
    single_data = await get_single(db['test_db_1'], 'name', 'John Doe', 'test_collection')
    logger.info(f"Single Data: {single_data}")


    field_to_update = {"age": 3}  # Example update operation: increment age by 1
    updated_data = await update_single(db['test_db_1'], field='name', value='John Doe', update=field_to_update, collection_name='test_collection')
    logger.info(f"Updated Data: {updated_data}")

    # Delete data by field
    #delete_count = await delete_single(db['test_db_1'], 'name', 'John Doe', 'test_collection')
    #logger.info(f"Deleted Count: {delete_count}")

    # Close connection
    await close()

# Run the main function
asyncio.run(main())

     

```