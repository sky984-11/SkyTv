import scrapy
from scrapy.http import Request
from urllib.parse import urlparse
import re
from parser_video.utils.api import Api
from parser_video.utils.tools import read_white_list
from parser_video.items import ParserVideoItem
from parser_video.utils.cache import MultiDBCacheManager

# 思考：如何减少请求次数(接口请求和网站请求)

class KekeSpider(scrapy.Spider):
    name = "keke"
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = Api()
        self.base_url = None
        self.white_list = read_white_list()
        self.cahce = MultiDBCacheManager()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.base_url = spider.api.get_source(spider.name).get('url')
        return spider

    def start_requests(self):
        if self.base_url:
            for title in self.white_list:
                search_url = f"{self.base_url}/search?os=pc&k={title}"
                yield Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"vod_title": title}
                )

    def extract_play_url(self, html):
        url_pattern = r'src:\s*"([^"]+)"'
        match = re.search(url_pattern, html)
        return match.group(1) if match else ""

    def parse(self, response):
        # yield {
        #         'play_from': 'keke',
        #         'play_status': True,
        #         'play_title': '玫瑰的故事',
        #         'play_url': 'https://172.80.104.114:11301/data6/files/hls/dhz/21/20556/24062019/909746/1920/index.m3u8?appId=kkdy&sign=a8ffad5de88bc7038c378e20494f3739&timestamp=1720416546',
        #         'vod_content': '\n'
        #             '                            出生于书香世家的黄亦玫（刘亦菲 '
        #             '饰）一路在呵护中长大，从小便展露出艺术天赋。初入职场的黄亦玫很快受到重用，与合作伙伴庄国栋相识相爱，但最终错过彼此，这段职场磨炼也令她对自己的人生有了更清晰的规划，决定重返校园求学深造。毕业后，她和学长方协文步入婚姻殿堂。可婚后两人发展方向相去甚远，最 '
        #             '终选择离婚。黄亦玫开始创业，在艺术品策展领域打拼出一片天地，在此期间还遇到了自己的灵魂伴侣溥家明，可溥家明只剩几个月的生命，两人这段爱情最终以生死离别画上句号。 '
        #             '但黄亦玫没有就此消沉，她还是一如既往地为活出更精彩的自己而努力着。\n'
        #             '                        ',
        #         'vod_episodes': '第28集',
        #         'vod_episodes_index': 28,
        #         'vod_pic_url': 'https://61.147.93.252:15002/vod1/vod/cover/20240603/12/48/06/717ceb0c8dfbdcf93a287e81a396db20.jpg',
        #         'vod_source': 'keke',
        #         'vod_tag': '2024/中国大陆/内地剧,剧情,国产剧,大陆剧',
        #         'vod_title': '玫瑰的故事',
        #         'vod_total_episodes': '已完结 番外',
        #         'vod_type': '剧集'
        #     }
        try:
            vod_title = response.meta['vod_title']
            video_list = response.css('a.search-result-item')
            for video in video_list:
                title_text = video.css('.title::text').get()
                if title_text == vod_title:
                    user_image_url = response.xpath('/html/body/div[1]/div[3]/div[1]/div[5]/a/img/@src').get()
                    parsed_url = urlparse(user_image_url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    next_url = ''.join([self.base_url,video.css('.search-result-item::attr(href)').get()])
 
                    yield Request(
                    url=next_url,
                    callback=self.parse_episodes,
                    meta={
                        "vod_title": vod_title,
                        "vod_pic_url": ''.join([base_url,video.css('img::attr(data-original)').get()]),
                        "vod_type":video.css('.search-result-item-header div::text').get(),
                        "vod_tag":'/'.join(video.css('.tags span::text').getall()),
                        "vod_content":video.css('.desc::text').get()
                    }
                )
        except Exception as e:
            self.logger.error(f"Error while parsing response for URL: {response.url}. Error: {e}")
            # 可以在这里添加重试机制，例如使用 response.request.meta['retry_times'] 来控制重试次数

    def parse_episodes(self,response):
        """
        爬取集数
        """
        vod_total_episodes = response.xpath(
            '/html/body/div[1]/div[3]/div[2]/div[2]/div[3]/div[6]/div[2]/text()').extract_first()
        response.meta['vod_total_episodes'] = vod_total_episodes

        episode_list_div= response.xpath('/html/body/div[1]/div[3]/div[2]/div[4]/div[2]/div[1]/a')
        vod_episodes_index = 1
        for data in episode_list_div: 
            vod_episodes = data.xpath('text()').get()
            response.meta['vod_episodes'] = vod_episodes
            response.meta['vod_episodes_index'] = vod_episodes_index

            next_url = ''.join([self.base_url,data.xpath('@href').get()])


            yield Request(
                    url=next_url,
                    callback=self.parse_player,
                    meta=response.meta
                )
            vod_episodes_index += 1 
        
    def parse_player(self, response):
        """
        爬取播放界面
        """
        play_url = self.extract_play_url(response.text)
        valid_meta = {k: v for k, v in response.meta.items() if k in ParserVideoItem.fields}
        item = ParserVideoItem(**valid_meta)
        item['play_url'] = play_url
        item['play_status'] = True
        item['play_from'] = self.name
        item['vod_source'] = self.name
        item['play_title'] = response.meta['vod_title']
        yield item