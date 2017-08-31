import scrapy

'''
Crawling strategy: We'll be crawling playlists from 'sitevagalume' users and from
all 'sitevagalume' followers
'''
# https://meu.vagalume.com.br/userData.php?action=getShowVincs&userID=3ade68b7g0ae7cea3&offset=0&typeFriend=followers


class VagalumeUsersSpider(scrapy.Spider):
    name = 'vagalumespider'
    start_urls = ['https://meu.vagalume.com.br/userData.php?action=getShowVincs&userID=3ade68b7g0ae7cea3&offset=0&typeFriend=followers']

    def __init__(self):
        self.count = 0
        self.user_file = open('vagalume_users.txt', 'a')

    def parse(self, response):
        if len(response.css('li')) > 0:
            for user in response.css('li'):
                self.user_file.write('%s\n' % user.css('::attr(href)').extract_first().replace('/','').strip())
            self.count+=1
            next_page = 'https://meu.vagalume.com.br/userData.php?action=getShowVincs&userID=3ade68b7g0ae7cea3&offset=%i&typeFriend=followers' % self.count
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        else:
            self.user_file.close()