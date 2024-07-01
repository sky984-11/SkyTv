'''
Description: 可可影视爬取
Author: sky
Date: 2024-06-30 10:32:22
LastEditTime: 2024-07-01 14:11:41
LastEditors: sky
'''
import scrapy  
from scrapy.http import Request
from urllib.parse import urlparse    
import re
from scrapy.utils.project import get_project_settings
  
class KekeSpider(scrapy.Spider):  

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(KekeSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.base_url = get_project_settings().get('KEKE_BASE_URL')
        return spider
    
    name = "keke_home"  
    _blacklist_cache = None

    def start_requests(self):
        '''起始url地址'''
        start_url = self.base_url
        yield scrapy.Request(url=start_url, callback=self.parse)

    def image_base_url(self, response):
        '''从首页获取图片的base_url'''
        user_image_url = response.xpath('/html/body/div[1]/div[3]/div[1]/div[5]/a/img/@src').get()
        parsed_url = urlparse(user_image_url)  
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}" 
        return base_url


    def parse(self, response):
        """
        解析响应，提取数据并生成新的请求。
        """
        image_base_url = self.image_base_url(response)

        # 定义类型映射
        type_mapping = {5: 1, 7: 0, 13: 2}  # movie: 1, tv_show: 0, anime: 2

        # 遍历首页的热门电影/电视剧/动漫，每种热门类别包含8个
        for i in range(1, 9):
            # 热门影视
            for tv in type_mapping.keys():
                hot_title_xpath = f'/html/body/div[1]/div[3]/div[2]/div[{tv}]/div[2]/div/div/div[{i}]/a/div[2]/div[2]/text()'
                hot_rating_xpath = f'/html/body/div[1]/div[3]/div[2]/div[{tv}]/div[2]/div/div/div[{i}]/a/div[1]/div[2]/div[1]/span/text()'
                hot_total_episodes_xpath = f'/html/body/div[1]/div[3]/div[2]/div[{tv}]/div[2]/div/div/div[{i}]/a/div[1]/div[3]/span/text()'
                hot_image_xpath = f'/html/body/div[1]/div[3]/div[2]/div[{tv}]/div[2]/div/div/div[{i}]/a/div[1]/div[1]/img/@data-original'
                hot_href_xpath = f'/html/body/div[1]/div[3]/div[2]/div[{tv}]/div[2]/div/div/div[{i}]/a/@href'
            
                title = response.xpath(hot_title_xpath).get()
                rating = response.xpath(hot_rating_xpath).get()
                total_episodes = response.xpath(hot_total_episodes_xpath).get().strip().replace('\n', '')
                image = response.xpath(hot_image_xpath).get()
                href = response.xpath(hot_href_xpath).get()

                # 动态获取type
                content_type = type_mapping[tv]

                yield Request(url=self.base_url + href, callback=self.parse_episodes, meta={
                    'title': title,
                    'rating': rating,
                    'total_episodes': total_episodes,
                    'image': image_base_url + (image or ''),  # 处理image可能为None的情况
                    'type': content_type,
                })

    def parse_episodes(self,response):
        """
        处理集数
        """
        tag_xpath = '/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/a'
        tag_list_div  = response.xpath(tag_xpath)
        tags = []
        for tag in tag_list_div:
            t = tag.xpath('.//text()').get()
            if t:
                tags.append(t.strip())

        tags_joined = '/'.join(tags)
        
        
        description_xpath = '/html/body/div[1]/div[3]/div[2]/div[2]/div[3]/div[1]/p/text()'
        description = response.xpath(description_xpath).get()
        
        # 获取传递的meta数据
        image = response.meta['image']
        title = response.meta['title']
        rating = response.meta['rating']
        type = response.meta['type']
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
                    'type': type
                })
            
    def parse_player(self, response):
        """
            处理播放界面，获取播放链接
        """
        # 获取传递的meta数据
        image = response.meta['image']
        title = response.meta['title']
        rating = response.meta['rating']
        type = response.meta['type']
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
                'type': type,
                'source': 'Keke',
                'link':link,
                'episode':episode,
                'tv_title':title,
                'tags':tags,
                'hot': True,
            }