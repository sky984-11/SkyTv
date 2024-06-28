import scrapy  
from scrapy.http import Request
from urllib.parse import urlparse    
import re
  
class KekeSpider(scrapy.Spider):  
    name = "keke"  
    allowed_domains = ["www.keke12.com"]
    base_url = "https://www.keke12.com:51111"
    start_urls = [base_url + "/show/1-----3-1.html"]  # 起始URL  
  
    def get_next_page_number(self, current_number):  
        # 假设页码是整数，并且从2开始（因为已经有一个3-2的页面了）  
        current_number = int(current_number.split('-')[-1])  
        return current_number + 1  
  
    def get_next_page_url(self, current_url):  
        # 提取页码部分并递增  
        page_match = current_url.rsplit('-', 1)[-1].rsplit('.', 1)[0]  # 提取'3-2'这样的页码  
        next_page_number = self.get_next_page_number(page_match)  
        # 构造新的URL  
        base_url = current_url.rsplit(page_match, 1)[0]  # 去掉页码部分  
        return f"{base_url}{next_page_number}.html"
    

    def parse_player(self, response):
        """
            处理播放界面，获取播放链接
        """
        # 获取传递的meta数据
        image = response.meta['image']
        title = response.meta['title']
        rating = response.meta['rating']
        total_episodes = response.meta['total_episodes']
        description = response.meta['description']
        episode = response.meta['episode']

        res = response.text
        url_pattern = r'src:\s*"([^"]+)"' 
        match = re.search(url_pattern, res) 
        
        if match:  
            link = match.group(1)  

        yield {
                'image': image,
                'title': title,
                'rating': rating,
                'total_episodes': total_episodes,
                'description': description,
                'type': 'movie',
                'source': 'keke',
                'link':link,
                'episode':episode,
                'tv_title':title
            }

    def parse_episodes(self,response):
        """
        处理集数
        """
        description_xpath = '/html/body/div[1]/div[3]/div[2]/div[2]/div[3]/div[1]/p/text()'
        description = response.xpath(description_xpath).get()
        
        # 获取传递的meta数据
        image = response.meta['image']
        title = response.meta['title']
        rating = response.meta['rating']
        total_episodes = response.meta['total_episodes']
        episode_list_xpath = '/html/body/div[1]/div[3]/div[2]/div[4]/div[2]/div[1]/a'
        episode_list_div = response.xpath(episode_list_xpath)

        for episode in episode_list_div: 
            href = episode.xpath('@href').get()
            episode = episode.xpath('.//text()').get()
            player_link = self.base_url + href
        
            yield Request(url=player_link, callback=self.parse_player, meta={
                    'image': image,
                    'title': title,
                    'rating': rating,
                    'total_episodes': total_episodes,
                    'description': description,
                    'episode':episode
                })
  
    def parse(self, response):  
        # 提取图片链接	https://61.147.93.252:15002/vod1/app/avatars/guest.png
        user_image_url = response.xpath('/html/body/div[1]/div[3]/div[1]/div[5]/a/img/@src').get()
        parsed_url = urlparse(user_image_url)  
        base_url_with_port = f"{parsed_url.scheme}://{parsed_url.netloc}" 
        #   
        for i in range(1, 2):  # 假设每页有18张图片（可能需要调整）  
            image_xpath = f'/html/body/div[1]/div[3]/div[2]/div[5]/div/div/div/div[{i}]/a/div[1]/div[1]/img/@data-original'
            title_xpath = f'/html/body/div[1]/div[3]/div[2]/div[5]/div/div/div/div[{i}]/a/div[1]/div[1]/img/@title'
            rating_xpath = f'/html/body/div[1]/div[3]/div[2]/div[5]/div/div/div/div[{i}]/a/div[1]/div[2]/div[1]/span/text()'
            total_episodes_xpath = f'/html/body/div[1]/div[3]/div[2]/div[5]/div/div/div/div[{i}]/a/div[1]/div[3]/span/text()'
            next_link_xpath = f'/html/body/div[1]/div[3]/div[2]/div[5]/div/div/div/div[{i}]/a/@href'
            next_link = self.base_url + response.xpath(next_link_xpath).get()

            total_episodes_text = response.xpath(total_episodes_xpath).get() 
            if total_episodes_text is not None:  
                total_episodes = total_episodes_text.strip().replace('\n', '')  
            else:  
                total_episodes = None  

            yield Request(url=next_link, callback=self.parse_episodes, meta={
                'image': base_url_with_port + response.xpath(image_xpath).get(),
                'title': response.xpath(title_xpath).get(),
                'rating': response.xpath(rating_xpath).get(),
                'total_episodes': total_episodes,
            })
                
        # 检查是否有下一页并请求  
        page_xpath = '/html/body/div[1]/div[3]/div[2]/div[6]/a[@class="page-item-next"]/text()'
        page_urls = response.xpath(page_xpath).get()  
        next_page_url = self.get_next_page_url(response.url)
        print(page_urls,next_page_url)
        if page_urls: 
            yield Request(url=next_page_url, callback=self.parse)