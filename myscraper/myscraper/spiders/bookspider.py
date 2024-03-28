import scrapy
from myscraper.items import BookItem  

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod') 
        for book in books:
            product_page_url = book.css('h3 a').attrib['href']
            
            if 'catalogue/' in product_page_url:
                book_url = "https://books.toscrape.com/" + product_page_url
                print(book_url)
            else:
                book_url = "https://books.toscrape.com/catalogue/" + product_page_url
                print(book_url)


            yield scrapy.Request(book_url, callback=self.parse_book_page)

        next_page = str(response.css('li.next a ::attr(href)').get())

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    

    def parse_book_page(self, response):
        book = response.css('div.product_main')[0]
        table_rows = response.css('table tr')
        book_item = BookItem()

        book_item['name'] = book.css('h1 ::text').get(),
        book_item['url' ]= response.url,
        book_item['price'] = book.css('p.price_color ::text').get(),
        book_item['description'] = book.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['upc'] = table_rows[0].css('td ::text').get(),
        book_item['Product Type'] = table_rows[1].css('td ::text').get(),
        book_item['price_excl_tax)'] = table_rows[2].css('td ::text').get(),
        book_item['price_incl_tax)'] = table_rows[3].css('td ::text').get(),
        book_item['tax'] = table_rows[4].css('td ::text').get(),
        book_item['availability'] = table_rows[5].css('td ::text').get(),
        book_item['number_of_reviews'] = table_rows[6].css('td ::text').get(),
        book_item['category'] = book.xpath('//ul[@class="breadcrumb"]/li[@class="active"]/preceding-sibling::li[1]/a/text()').get()

        yield book_item
