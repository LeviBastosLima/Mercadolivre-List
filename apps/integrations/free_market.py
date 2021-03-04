import os
from typing import List, Tuple
import asyncio

import aiohttp
import requests


class FreeMarket:
    _MERCADO_LIBRE_API_URL = os.environ.get('MERCADO_LIBRE_API_URL',
                                            'https://api.mercadolibre.com/')

    _url_request_to_category = '{mercado_libre_url}sites/MLA/search?category=MLA420040' \
                               '&sort=price_desc'.format(mercado_libre_url=_MERCADO_LIBRE_API_URL)
    _total = 0

    def get_users_and_publications(self) -> Tuple[List[dict], List[dict]]:
        publications = self._get_top_ten_publications()
        users = self._get_top_ten_users()
        return publications, users

    def _get_top_ten_users(self) -> List[dict]:
        users = self._get_all_users()
        users = reversed(sorted(users, key=lambda i: i['sales']))
        users = [obj for obj in users]
        users = users[:10] if len(users) > 10 else users
        return users

    def _get_all_users(self) -> List[dict]:
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

    def _get_top_ten_publications(self) -> List[dict]:
        request = requests.get(self._url_request_to_category + '&limit=10').json()
        results = request.get('results', False)
        self._total = request.get('paging').get('total')
        results = [{
            'title': results[i].get('title'),
            'price': "${:,}".format(results[i].get('price')).replace(',', '.'),
            'link': results[i].get('permalink')
        } for i in range(0, 10)]
        return results

    async def _fetch(self, session, url):
        """Execute an http call async
        """
        async with session.get(url) as response:
            resp = await response.json()
            return resp

    async def _fetch_all(self, urls):
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
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return responses

    def _get_all_data(self):
        urls = ['{}&offset={}&limit=50'.format(self._url_request_to_category, i) for i in range(0, self._total, 50)]
        responses = asyncio.run(self._fetch_all(urls))
        return responses
