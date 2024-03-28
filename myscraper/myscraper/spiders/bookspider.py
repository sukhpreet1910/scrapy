import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod') 
        for book in books:
            yield{
                'name' : book.css('h3 a::text').get(),
                'price': book.css('div.product_price p.price_color::text').get(),
                'url' : book.css('h3 a').attrib['href']
            } 
        next_url = response.css('li.next a ::attr(href)').get()
        print(next_url)
        # if next_url:
        #     print(next_url)
        #     if 'catalogue/' in next_url:
        #         next_page_url = 'https://books.toscrape.com/' + next_url
        #         print(next_page_url)
        #     else:
        #         next_page_url = 'https://books.toscrape.com/catalogue/' + next_url
        #         print(next_page_url)
        #     yield response.follow(next_page_url, callback = self.parse)


        if next_url is not None:
            if 'catalogue/' in next_url:
                # next_page_url = f"https://books.toscrape.com/{next_url}"
                next_page_url = "https://books.toscrape.com/" + str(next_url)

            else:
                # next_page_url = f"https://books.toscrape.com/catalogue/{next_url}"
                next_page_url = "https://books.toscrape.com/catalogue/" + str(next_url)

            yield response.follow(next_page_url, callback=self.parse)
        

