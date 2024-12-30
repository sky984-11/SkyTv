import subprocess
import os

basedir = os.path.abspath(os.path.dirname(__file__))
subprocess.run(['scrapy', 'crawl', 'sync_player_url'], cwd=basedir)