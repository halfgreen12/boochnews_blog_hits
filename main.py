from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

from pathlib import Path


# pathlib file path
file_name = '09-22'
filepath = Path(f'/Users/HP/Downloads/{file_name}.csv')

# connect to http://www.boochnews.com/stats/awstats/
html_text = requests.get('http://www.boochnews.com/stats/awstats/2022-09/awstats.www.boochnews.com.urldetail.html',
                         auth=('[username]', '[password]')).text

# initialize beautiful soup and define table
soup = BeautifulSoup(html_text, 'lxml')
table = soup.find('table', class_='aws_border sortable')

# define headers of columns ('th' references headers)
headers = []
for i in table.find_all('th')[0:5]:
    title = i.text
    headers.append(title)

# define pandas dataframe
df = pd.DataFrame(columns=["Blog Post URL", "Viewed", "Average size", "Entry", "Exit"])

# empty list to append queried links to
blog_posts = []

# loop through each row and return list
for row in table.find_all('tr')[3:]:
    data = row.find_all('td')
    row_data = [td.text.strip() for td in data]
    row_data.pop()
    # print(data)

    # sort through and return relevant posts to blog_posts list
    url = row_data[0]
    if url.startswith('/20') and re.search('[a-zA-Z]', url) or url.startswith('/kombucha-brewers-worldwide/')\
            or url.startswith('/what-is-kombucha/') or url.startswith('/our-mission/')\
            or url.startswith('/category/about-kombucha/') or url == '/':

        # replace first element of row_data list with the full url for boochnews.com link
        row_data_join_booch = ''.join('https://www.boochnews.com' + row_data[0])
        row_data[0] = row_data_join_booch
        blog_posts.append(row_data)

# unpack nested lists to insert into dataframe
for blog_post in blog_posts:
    df.loc[len(df)] = blog_post

# export pandas dataframe as csv file to path defined on lines 12 and 13
df.to_csv(filepath)

