import asyncio
from src import Pipeline

if __name__ == '__main__':
    pipeline = Pipeline()
    asyncio.run(pipeline.run())