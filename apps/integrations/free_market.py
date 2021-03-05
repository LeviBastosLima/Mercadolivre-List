import os
import asyncio
from typing import List, Tuple

import aiohttp
import requests


class FreeMarket:
    _FREE_MARKET_API_URL: str = os.environ.get('MERCADO_LIBRE_API_URL',
                                               'https://api.mercadolibre.com/')

    _url_request_to_category: str = '{mercado_libre_url}sites/MLA/search?category=MLA420040' \
                                    '&sort=price_desc'.format(mercado_libre_url=_FREE_MARKET_API_URL)
    _total: int = 0

    def get_users_and_publications(self) -> Tuple[List[dict], List[dict]]:
        """Calls methods to return the highest sales and users
        """
        publications = self._get_highest_ten_publications()
        users = self._get_highest_ten_users()
        return publications, users

    def _get_highest_ten_users(self) -> List[dict]:
        """return highest ten users
        """
        users = self._get_all_users()
        users = list(reversed(sorted(users, key=lambda i: i['sales'])))
        users = users[:10] if len(users) > 10 else users
        return users

    def _get_all_users(self) -> List[dict]:
        """Checks all salespeople in the category and adds the total number
            of sales for each
        """
        all_data = self._get_all_data()
        results = []
        for obj in all_data:
            result = obj.get('results', False)
            if result:
                results.extend(result)
        results = results[:self._total]

        list_nickname = []
        list_sales = []
        for obj in results:
            permalink = obj.get('seller').get('permalink', False)
            if permalink:
                nickname = permalink.split('/')[3].replace('+', ' ')
                sales = obj.get('sold_quantity')
                if nickname in list_nickname:
                    index = list_nickname.index(nickname)
                    list_sales[index] += sales
                else:
                    list_nickname.append(nickname)
                    list_sales.append(sales)
        response = zip(list_nickname, list_sales)
        response = [{
            'nick_name': nickname,
            'sales': sales
        } for nickname, sales in response]
        return response

    def _get_highest_ten_publications(self) -> List[dict]:
        """Returns the ten most expensive items
        """
        request = requests.get(self._url_request_to_category + '&limit=10').json()
        results = request.get('results', False)
        self._total = request.get('paging').get('total')
        results = [{
            'title': results[i].get('title'),
            'price': "${:,}".format(results[i].get('price')).replace(',', '.'),
            'link': results[i].get('permalink')
        } for i in range(0, 10)]
        return results

    async def _fetch(self, session: aiohttp.ClientSession, url: str) -> List[dict]:
        """Execute an http call async
        """
        async with session.get(url) as response:
            return await response.json()

    async def _fetch_all(self, urls: List[str]) -> tuple:
        """ Gather many HTTP call made async
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                tasks.append(
                    self._fetch(
                        session,
                        url,
                    )
                )
            responses = await asyncio.gather(*tasks, return_exceptions=False)
            return responses

    def _get_all_data(self) -> List[dict]:
        """call the __fetch_all method and return all sales of category
        """
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        urls = ['{}&offset={}&limit=50'.format(self._url_request_to_category, i) for i in range(0, self._total + 50, 50)]
        responses = loop.run_until_complete(self._fetch_all(urls))
        loop.stop()
        return responses
