'''
Description: 
Author: sky
Date: 2024-08-02 11:18:26
LastEditTime: 2024-08-02 11:18:47
LastEditors: sky
'''
import subprocess
import os

basedir = os.path.abspath(os.path.dirname(__file__))
subprocess.run(['scrapy', 'crawl', 'keke'], cwd=basedir)