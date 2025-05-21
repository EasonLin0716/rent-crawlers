import sys
import os
import time
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from libs.utils import get_page_content, write_file, use_selenium, render_images, render_link
load_dotenv()

def write_normal(driver, start_url):
  def _helper(start_page, data):
    page = start_page
    while True:
        soup = get_page_content(driver, start_url.replace('/1.html', f'/{page}.html'))
        items = soup.select('#buy_container .ddhouse')
        if not items:
            break
        for item in items:
            image_lst = []
            img_count = int(item.select_one('div.img_count_txt').text)
            first_image_src = item.select_one('.item_img img').get('src')
            for i in range(0, img_count):
                if chr(65 + i) in ['E', 'F']:
                    img_count += 1
                    continue
                current_image_src = first_image_src.replace('A', chr(65 + i))
                image_lst.append(current_image_src)
            title = item.select_one('.item_title').text
            link = item.select_one('a')['href']
            areaAndFloor = item.select_one('.detail_line2')
            area = areaAndFloor.select('span')[2].text.replace('\n', '')
            floor = areaAndFloor.select('span')[4].text.replace('\n', '')
            address = item.select('.detail_line2')[1].text.replace('\n', '')
            price = item.select_one('.detail_price').text.replace('\n', '')
            data.append([title, price, address, floor, area, image_lst, link])
        page += 1
    return data
        
  data = _helper(1, [])
  columns = ['title', 'price', 'address', 'floor', 'area', 'images', 'link']
  df = pd.DataFrame(data, columns=columns)
  json_output = df.to_json(orient='records')
  write_file(json_output, 'sinyi.json')
  df['images'] = df['images'].apply(render_images)
  df['link'] = df.apply(lambda x: render_link(x['link'], x['title']), axis=1)
  html_output = df.to_html(escape=False)
  write_file(html_output, 'sinyi.html')
  print('write normal done')

def main():
    driver = use_selenium()
    start_url = os.getenv('SINYI_FILTER_URL')
    if (start_url is None):
        print('Please set SINYI_FILTER_URL in .env')
        print('If .env is not exist, please create one at the root directory')
        print('Example: SINYI_FILTER_URL=https://www.sinyi.com.tw/rent/list/Taipei-city/103-zip/index.html')
        sys.exit()
    start_url = start_url.replace('/index.html', '/1.html')
    write_normal(driver, start_url)

main()