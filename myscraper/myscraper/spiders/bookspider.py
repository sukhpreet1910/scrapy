import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod') 
        for book in books:
            product_page_url = book.css('h3 a').attrib['href']
            
            if 'catalogue/' in product_page_url:
                book_url = "https://books.toscrape.com" + str(product_page_url)
            else:
                book_url = "https://books.toscrape.com/catalogue/" + str(product_page_url)

            yield scrapy.Request(book_url, callback=self.parse_book_page)

        next_page = response.css('li.next a ::attr(href)').get()

        if next_page:
            if 'catalogue/' in next_page:
                next_page_url = "https://books.toscrape.com" + str(next_page)
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + str(next_page)
            yield response.follow(next_page_url, callback=self.parse)

    

    def parse_book_page(self, response):
        book = response.css('div.product_main')[0]
        table_rows = response.css('table tr')

        yield{
            'name' : book.css('h1 ::text').get(),
            'url' : response.url,
            'price' : book.css('p.price_color ::text').get(),
            'description' : book.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'upc' : table_rows[0].css('td ::text').get(),
            'Product Type' : table_rows[1].css('td ::text').get(),
            'Price (excl. tax)' : table_rows[2].css('td ::text').get(),
            'Price (incl. tax)' : table_rows[3].css('td ::text').get(),
            'Tax' : table_rows[4].css('td ::text').get(),
            'Availability' : table_rows[5].css('td ::text').get(),
            'Number of reviews' : table_rows[6].css('td ::text').get(),
            'Category' : book.xpath('//ul[@class="breadcrumb"]/li[@class="active"]/preceding-sibling::li[1]/a/text()').get()
        }
            

        
        next_url = response.css('li.next a ::attr(href)').get()
    
        if next_url is not None:
            if 'catalogue/' in next_url:
                # next_page_url = f"https://books.toscrape.com/{next_url}"
                next_page_url = "https://books.toscrape.com/" + str(next_url)

            else:
                # next_page_url = f"https://books.toscrape.com/catalogue/{next_url}"
                next_page_url = "https://books.toscrape.com/catalogue/" + str(next_url)

            yield response.follow(next_page_url, callback=self.parse)
        

