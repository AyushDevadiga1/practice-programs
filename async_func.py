import asyncio
import time
async def fetch_data_sync(api_name):
    print(f" Starting requests for api : {api_name} " )
    await asyncio.sleep(2)
    print(f"Finished the requesr for :{api_name} " )
    return f"{api_name} data "

async def main():
    start = time.time()
    results = await asyncio.gather (
					fetch_data_sync("API_1"),
					fetch_data_sync("API_2"),
					fetch_data_sync("API_3")
					)
    end = time.time()
    print(f" The time required to run this is : {end-start} seconds ")
asyncio.run(main())