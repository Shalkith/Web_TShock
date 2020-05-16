import requests, wget
from bs4 import BeautifulSoup as bs

url = 'https://terraria.fandom.com/wiki/Image_Database'
data = requests.get(url)
data2 = data.text
soup = bs(data2, 'html.parser')


trs = soup.findAll('tr')
images = []
for x in trs:
    string=str(x)
    if ".png" in string.lower():
        try:
                string = bs(string, 'html.parser')
                tds = []
                tds = string.findAll('td')
                zone1 = str(tds[0])
                zone2 = str(tds[1])
                zone3 = str(tds[2])

                picurl = zone1.split('href="')[1].split('/revision')[0]
                filename = zone3.split('">')[1].split('</a>')[0].replace(" ",'_')+'.png'
                r = requests.get(picurl, allow_redirects=True)

                open('static/images/icons/'+filename, 'wb').write(r.content)
                
                #input('...')
                #images.append(string)
        except Exception as e:
            print('Error:',e)
            

