
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
from selenium.webdriver.support.ui import Select

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







# requests download image (file)
import shutil
import requests
session = requests.Session()
def download_image(url, path):
  print(f'download img {url} ...')
  r = session.get(url, stream=True)
  if r.status_code == 200:
    with open(path, 'wb') as f:
      r.raw.decode_content = True
      shutil.copyfileobj(r.raw, f)
  print('done')


def download_image2(url, folder, name, referer):
    print(f'download img {url} ...')
    default_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"}
    headers = {"Referer": referer}
    resp = session.get(url, headers={**default_headers, **headers}, stream=True)
    image_body = resp.content
    with open(f'{folder + "/" + name}', "wb") as f:
        f.write(image_body)
    print(f'get image {name} done')






sess = requests.Session()
def download_image3(url, output_folder, image_name, referer):
    # 先检查是否已经存在
    # 使用 referer 
    # 使用 socks proxies     # pip install requests[socks]
    output_file = os.path.join(output_folder, image_name)
    if os.path.exists(output_file):
        print(f'{image_name} already exists, skip')
        return

    proxies = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080',
    }
    default_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"}
    headers = {"Referer": referer}
    print(f'download img {url} ...')

    response = sess.get(url, headers={**default_headers, **headers}, stream=True, proxies=proxies)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
    print(f'  done download {output_file}')






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





def http_get(url, headers, session, use_cache=True, cookies=None) -> str:
    if use_cache:
        # 简单的本地文件当缓存
        filecache = FileCache.load_from(folder='.cache')
        if hit := filecache.find(url):
            return hit
        else:
            result = http_get(url, headers, session, use_cache=False, cookies=cookies)
            return filecache.save(url, result)
    else:
        default_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"}
        resp = session.get(url, headers={**default_headers, **headers}, cookies=cookies)
        return resp.content.decode('utf-8')





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

# extract from pq object
author_id = doc.find('h3.mp-info__title>a').attr('href').split('/')[-1]
# extract from lxml object
# for div in doc.find(...)
author_id = div.attrib['href'].split('/')[-1]



"""
sample
selenium custom driver
css selector
"""

# selenium custom driver
def get_windows_firefox_driver():
  gecko_path = '/Users/probe/git/geckodriver'
  gecko_path = 'C:/Program Files/Mozilla Firefox/geckodriver.exe'
  profile = webdriver.FirefoxProfile()
  # profile.set_preference("browser.download.dir","/Users/probe/git/Crawler/");
  # profile.setPreference("browser.download.folderList", 2);
  profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,text/csv");
  profile.set_preference("browser.download.dir",os.getcwd())

  # if proxies:
  #   profile.set_preference("network.proxy.type", 1)
  #   profile.set_preference("network.proxy.socks", "127.0.0.1")
  #   profile.set_preference("network.proxy.socks_port", 1080)
  #   profile.set_preference("network.proxy.socks_version", 5)
  #   # profile.setAssumeUntrustedCertificateIssuer(False)
  #   profile.update_preferences()
  driver = webdriver.Firefox(firefox_profile=profile,
                             executable_path=gecko_path)
  return driver


class DriverFindElementByCSS:
  ''' usage:
      driver / css(pat)  => one element
      driver // css(pat)  => [element list]
  '''
  def __call__(self, pat):
    self.pat = pat
    return self
  def __rtruediv__(self, driver):
    return driver.find_element_by_css_selector(self.pat)
  def __rfloordiv__(self, driver):
    return driver.find_elements_by_css_selector(self.pat)
css = DriverFindElementByCSS()


def fetch_one_page(driver, state_code):
  driver.get('https://ofmpub.epa.gov/apex/sfdw/f?p=108:200::::::')
  print('get US map page...')
  # state_code = '09'
  selector = Select(driver / css('#P200_STATE'))
  selector.select_by_value(state_code)
  search_button = driver / css('#P200_SEARCH')
  search_button.click()
  print('click search button...')
  WebDriverWait(driver, 120).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '#SFDWIR_row_select'))
  )
  change_all_selector = Select(driver / css('#SFDWIR_row_select'))
  change_all_selector.select_by_value('100000')
  print('click show all rows...')
  WebDriverWait(driver, 120).until(
      EC.invisibility_of_element_located((By.CSS_SELECTOR, 'span.u-Processing-spinner'))
  )
  WebDriverWait(driver, 400).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '.t-fht-tbody'))
  )

  time.sleep(10)
  print('prepare to fetch')
  tables_header, tables_body = driver // css('.a-IRR-table')
  headers = [td.text.replace('\n', ' ') for td in tables_header // css('th')]


  content = []
  for row in PyQuery(tables_body.get_attribute('outerHTML'))('tr'):
    row = PyQuery(row)
    if not row:
      continue
    row = [td.text for td in row('td')]
    if row and row[0]:
      content.append(row)
  record_csv(headers, content, 'epa_water_system_summary_{}_[{}].csv'.format(state_code, len(content)))


state_codes = '''
  AK AL AR AZ CA CO CT DC DE FL GA HI IA ID IL IN KS KY LA MA MD ME MI MN MO MS MT NC ND NE NH NJ NM NV NY OH OK OR PA RI SC SD TN TX UT VA VT WA WI WV WY AS MP PR VI 01 02 03 04 05 06 07 08 09 10 NN
'''.strip().split(' ')
driver = get_windows_firefox_driver()
for state_code in state_codes[:3]:
  fetch_one_page(driver=driver, state_code=state_code)
  


def usage_diskcache():
    '''基于文件的缓存用法'''
    import feedparser
    from diskcache import Cache
    cache = Cache(directory='.cache')

    def measure_time(func):
        import time
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"{func.__name__} 耗时: {elapsed_time} 秒")
            return result
        return wrapper

    @cache.memoize(typed=True, expire=1, tag='fib')
    def fibonacci(number):
        if number == 0:
            return 0
        elif number == 1:
            return 1
        else:
            return fibonacci(number - 1) + fibonacci(number - 2)

    @cache.memoize(typed=True, expire=3600, tag='feed')
    def feed_craw(url):
        return feedparser.parse(url)

    @measure_time
    def test_cache():
        cache.stats(enable=True)  # 首先开启统计

        print(sum(fibonacci(value) for value in range(35)))
        data = feed_craw('https://forum-zh.obsidian.md/c/8-category/8.rss')
        print(data.channel)

        hits, misses = cache.stats(enable=False, reset=True)
        print(f"stats {hits=}, {misses=}, {cache.volume()//1024}KB <{cache._directory}>")  # => hits=21, misses=3, 170KB <.cache>

    test_cache()
