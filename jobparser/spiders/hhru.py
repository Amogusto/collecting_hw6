import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ["https://hh.ru/search/vacancy?text=Python&from=suggest_post&area=1"]

    def parse(self, response:HtmlResponse):

        links = response.xpath("//a[@class='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath(" //a[@data-qa='pager-next']/href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@data-qa='vacancy_salary']/span/text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)