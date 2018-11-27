import os

import requests
from bs4 import BeautifulSoup

# p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# p1 = os.path.dirname(os.path.abspath(__file__))

# print(p)
# print(p1)

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}

url = 'https://www.theonion.com/'

#  content has the html of the page
content = session.get(url, verify=False).content

soup = BeautifulSoup(content, "html.parser")

posts = soup.find_all(
    'div', {'class': 'curation-module__item'})  # returns a list

# change the path as per your need (saurabh)
# media_root = '/Users/matthew/Downloads/dashboard/media_root'
# image_source = https://i.kinja-img.com/gawker-media/image/upload/s--gYN45W06--/
# c_fill,f_auto,fl_progressive,g_center,h_264,q_80,w_470/rf34mz2lzqhoxfgzqrgh.jpg
media_root = '/home/saurabh/django_projects/dashboard_project/src/media_root'

print(len(posts))

# for i in posts:

#     link = i.find_all('a', {'class': 'js_curation-click'})[1]['href']
#     title = i.find_all('a', {'class': 'js_curation-click'})[1].text
#     image_source = i.find('img', {'class': 'featured-image'})['data-src']

#     # stackoverflow solution, download image and put in local media_root
#     if not image_source.startswith(("data:image", "javascript")):
#         local_filename = image_source.split('/')[-1].split("?")[0]
#         r = session.get(image_source, stream=True, verify=False)
#         with open(local_filename, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=1024):
#                 f.write(chunk)

#         current_image_absolute_path = os.path.abspath(local_filename)
#         shutil.move(current_image_absolute_path, media_root)

#     # end of stackoverflow

#     new_headline = Headline()
#     new_headline.title = title
#     new_headline.url = link
#     new_headline.image = local_filename
#     new_headline.save()
