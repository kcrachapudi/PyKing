import asyncio
import time
    
async def make_rice():
    print("Starting to make_rice...")
    await asyncio.sleep(3)
    print("Rice is done!")

async def make_dal():
    print("Starting to make_dal...")
    await asyncio.sleep(4)
    print("Dal is done!")

async def make_roti():
    print("Starting to make_roti...")
    await asyncio.sleep(3)
    print("Roti is done!")
    
async def make_dessert():
    print("Starting to make_dessert...")
    await asyncio.sleep(1)
    print("Dessert is done!")

async def make_coffee():
    print("Starting to make_coffee...")
    await asyncio.sleep(2)
    print("Coffee is done!")

async def cook():
    start_time = time.perf_counter()

    print("Cooking Started...")
    await make_rice()
    await make_dal()
    await make_coffee()
    await make_roti()
    await make_dessert()

    end_time = time.perf_counter()
    print(f"Cooking is done in {end_time - start_time:.2f} seconds!")

async def smart_cook():
    start_time = time.perf_counter()

    print("Smart Cooking Started...")
    tasks = [
        make_rice(),
        make_dal(),
        make_coffee(),
        make_roti(),
        make_dessert()
    ]
    await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    print(f"Smart Cooking is done in {end_time - start_time:.2f} seconds!")

# Wrapper to run both one after the other
async def main():
    await cook()
    await smart_cook()

if __name__ == "__main__":
    asyncio.run(main())
