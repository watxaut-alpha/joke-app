import logging
import time

import scrapy
from scrapy.http.response import Response

logger = logging.getLogger('jokeBot')


class MilChistesSpider(scrapy.Spider):
    """
    """
    name = "MilChistes"
    allowed_domains = ["1000chistes.com"]

    start_urls = [
        'https://www.1000chistes.com/chistes-cortos/pagina/1'
    ]

    def parse(self, response: Response):

        # list of jokes in main page
        l_jokes = response.css('article[class="chiste mb10"]')

        # this will tell if we arrived at the last joke page or not
        if l_jokes:
            # get all the jokes in string
            for joke in l_jokes:
                l_strings = [x.get() for x in joke.css("p[itemprop='articleBody']::text")]
                s_joke = "".join(l_strings)
                url_id = joke.css("a[class='compartir']::attr('href')")[0].get()

                d_joke = {
                    "tweet_str_id": url_id,
                    "user_str_id": "1000Chistes",
                    "user_name": "1000Chistes",
                    "joke": s_joke
                }

                yield d_joke

            time.sleep(5)

            # follow onto the next page
            new_page_number = int(response.url.split(r"/")[-1]) + 1
            new_url = "{url}/{page_num}".format(
                url=r"/".join(response.url.split(r"/")[:-1]),
                page_num=new_page_number
            )
            print(new_url)
            yield response.follow(new_url, self.parse)
