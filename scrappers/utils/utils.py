from playwright.async_api import async_playwright
from httpx import HTTPStatusError, RequestError
from urllib.parse import urlparse
from datetime import datetime
import asyncio
import httpx
import os
import re

async def get_page_data(url, retries=5, backoff_factor=1.0, timeout=10.0):
    """
    Fetch a URL with retries and exponential backoff.

    Args:
        url (str): The URL to fetch.
        retries (int): Number of retries before giving up.
        backoff_factor (float): Factor by which the wait time increases after each retry.
        timeout (float): Timeout for the request in seconds.

    Returns:
        str: The HTML content of the page if successful.

    Raises:
        Exception: If all retries fail.
    """

    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url)
                response.raise_for_status() 

                parsed_url = urlparse(url)
                domain_name = re.sub(r"[^\w.-]", "_", parsed_url.netloc)
                formatted_current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_file = f"page_logs/{domain_name}_{formatted_current_datetime}.png"
                
                await take_full_page_screenshot(url, output_file=output_file)
                return response.content
        except (HTTPStatusError, RequestError) as e:
            print(f"Attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                sleep_time = backoff_factor * (8 ** attempt)
                print(f"Retrying in {sleep_time:.2f} seconds...")
                await asyncio.sleep(sleep_time)
            else:
                print("Max retries reached. Failing...")
                raise

async def take_full_page_screenshot(url: str, output_file: str):
    # Ensure directory exists
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="load")

        await page.screenshot(path=output_file, full_page=True)

        print(f"Screenshot saved as {output_file}")
        await browser.close()