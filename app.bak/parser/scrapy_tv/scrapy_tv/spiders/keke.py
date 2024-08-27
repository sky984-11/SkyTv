import scrapy  
from scrapy.http import Request
from urllib.parse import urlparse    
import re
from scrapy.utils.project import get_project_settings
  
class KekeSpider(scrapy.Spider):  

    # 使用from_crawler方法动态设置name和base_url
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(KekeSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.base_url = get_project_settings().get('KEKE_BASE_URL')
        return spider
    
    name = "keke"  
    allowed_domains = ["www.keke12.com"]
    _blacklist_cache = None

    def start_requests(self):
        # 现在可以使用self.base_url了
        start_url = f"{self.base_url}/show/1-----1-1.html"
        yield scrapy.Request(url=start_url, callback=self.parse)

    def read_blacklist(self):
        # 如果缓存中已有黑名单数据，则直接返回
        if self._blacklist_cache is not None:
            return self._blacklist_cache
        
        # 打开黑名单文件
        with open('./scrapy_tv/spiders/blacklist', 'r') as file:
            # 读取文件中的每一行，去除空白行、注释行及空字符
            blacklist = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            # 将处理后的黑名单存储到缓存中
            self._blacklist_cache = blacklist
            return blacklist
 
  
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
        tags = response.meta['tags']

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
                'tv_title':title,
                'tags':tags
            }

    def parse_episodes(self,response):
        """
        处理集数
        """
        blacklist = response.meta['blacklist']
        tag_xpath = '/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/a'
        tag_list_div  = response.xpath(tag_xpath)
        tags = []
        for tag in tag_list_div:
            t = tag.xpath('.//text()').get()
            if t in blacklist:
                return
            if t:
                tags.append(t.strip())

        tags_joined = '/'.join(tags)
        
        
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
                    'episode':episode,
                    'tags':tags_joined,
                })
  
    def parse(self, response):  
        # 提取图片链接	https://61.147.93.252:15002/vod1/app/avatars/guest.png
        user_image_url = response.xpath('/html/body/div[1]/div[3]/div[1]/div[5]/a/img/@src').get()
        parsed_url = urlparse(user_image_url)  
        base_url_with_port = f"{parsed_url.scheme}://{parsed_url.netloc}" 
        
        blacklist = self.read_blacklist()
        for i in range(1, 18):  # 假设每页有18张图片（可能需要调整）  
            image_xpath = f'/html/body/div[1]/div[3]/div[2]/div[5]/div/div/div/div[{i}]/a/div[1]/div[1]/img/@data-original'
            title_xpath = f'/html/body/div[1]/div[3]/div[2]/div[5]/div/div/div/div[{i}]/a/div[1]/div[1]/img/@title'
            title = response.xpath(title_xpath).get()

            if title in blacklist: #在黑名单中，跳过该影片
                continue

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
                'title': title,
                'rating': response.xpath(rating_xpath).get(),
                'total_episodes': total_episodes,
                'blacklist':blacklist
            })
                
        # 检查是否有下一页并请求  
        page_xpath = '/html/body/div[1]/div[3]/div[2]/div[6]/a[@class="page-item-next"]/text()'
        page_urls = response.xpath(page_xpath).get()  
        next_page_url = self.get_next_page_url(response.url)
        # print(page_urls,next_page_url)
        if page_urls: 
            yield Request(url=next_page_url, callback=self.parse)