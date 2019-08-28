
# crawler common import

import requests
sess = requests.Session()

import html2text

from pyquery import PyQuery as pq

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxProfile

from peewee import SqliteDatabase
from peewee import CharField
from peewee import DateField
from peewee import TextField
from peewee import IntegerField
from peewee import DateTimeField
from peewee import FloatField
from peewee import ForeignKeyField
from peewee import fn
from peewee import BooleanField
from peewee import Model
from peewee import fn
from peewee import JOIN





# requests download image
import shutil
def download_image(url, path):
  print(f'download img {url} ...')
  r = sess.get(url, stream=True)
  if r.status_code == 200:
    with open(path, 'wb') as f:
      r.raw.decode_content = True
      shutil.copyfileobj(r.raw, f)
  print('done')




# requests with UA
import requests
session = requests.Session()
def get_with_ua(url):
  UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
  headers = { "User-Agent" : UA, "Referer": "https://zhuanlan.zhihu.com/"}
  session = requests.Session()
  return session.get(url, headers=headers)

# after get response:
# resp = session.get(url, headers=headers)
text_data = resp.text                   # for text
text_data = bytes.decode(resp.content)  # for text

import json
json_data = json.loads(bytes.decode(resp.content, encoding='utf-8'))  # for json
json_data = resp.json()                                               # for json





def async_fetch_images_sample():
  import asyncio
  import aiohttp
  session = aiohttp.ClientSession()
  async def fetch_photo(index, name, url):
    print('async get photo {index} {name} {url}'.format(**locals()))
    async with session.get(url) as resp:
      image_body = await resp.read()
      with open("[{index}] {}.jpg".format(index, name), "wb") as f:
        f.write(image_body)
    print('async get photo {index} {name} done'.format(**locals()))

  def run_async_tasks(tasks):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*tasks))

  tasks = [fetch_photo(index, name, url) for index, name, url in parse_photos(content)]
  run_async_tasks(tasks)





# pyquery sample
doc = pq(htmltext)
for div in doc.find('#content-text > .tabbertab'):
  title = div.attrib['title']  # type(div.attrib) == dict
  pqdiv = pq(div)
  pqdiv.text()  # pq obj method





