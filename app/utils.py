from datetime import date, datetime
import aiohttp
import asyncio

def countdown(release):

    base = str(date.today())
    release_d = release
    release_date = datetime.strptime(release_d, "%Y-%m-%d")
    today = datetime.strptime(base, "%Y-%m-%d")

    difference = release_date - today
    countdown = difference.days
    return countdown if countdown >= 0 else -1



# async functions for multiple get requests to the tmdb api - used when rendering the user dashboard

async def fetch(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.json()

async def fetch_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(session, url)) 
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main(tv_ids, urls):    
    async with aiohttp.ClientSession() as session:
        responses = await fetch_all(session, urls)
        # print(list(responses))
        return list(responses)

def async_get_multiple(tv_ids, urls):
    responses = asyncio.run(main(tv_ids, urls))
    return responses
