import os
import time
import requests
import concurrent.futures
import asyncio
import aiohttp
import argparse

def download_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = url.split("/")[-1]
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Downloaded: {filename}")

def download_image_multithread(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, urls)

def download_image_multiprocess(urls):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(download_image, urls)

async def download_image_async(url, session):
    async with session.get(url) as response:
        filename = url.split("/")[-1]
        with open(filename, "wb") as file:
            file.write(await response.read())
        print(f"Downloaded: {filename}")

async def download_images_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(url, session) for url in urls]
        await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description="Download images from specified URLs.")
    parser.add_argument("urls", nargs="+", help="List of image URLs")
    args = parser.parse_args()

    start_time = time.time()

    print("Downloading images using multithreading:")
    download_image_multithread(args.urls)
    print(f"Multithreading Time: {time.time() - start_time:.2f} seconds\n")

    start_time = time.time()

    print("Downloading images using multiprocessing:")
    download_image_multiprocess(args.urls)
    print(f"Multiprocessing Time: {time.time() - start_time:.2f} seconds\n")

    start_time = time.time()

    print("Downloading images using asynchronous approach:")
    asyncio.run(download_images_async(args.urls))
    print(f"Asynchronous Time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
