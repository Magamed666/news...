import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
from playwright.async_api import async_playwright
import asyncio


async def main():
    # playwright = await async_playwright().start()
    # browser = await playwright.chromium.launch(headless=False)
    # page = await browser.new_page()
    # await page.goto("https://www.reuters.com/")
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.reuters.com/")
        await page.wait_for_timeout(1000)
        print('hello')
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.select('ul'))
        

if __name__ == '__main__':
    asyncio.run(main())

