from bs4 import BeautifulSoup
from urllib import request
from json import dumps

l = list()

raw = {
    'link': '',
    'dump': '',
    'title': '',
    'subtitle': '',
    'overview': '',
    'rent': '',
    'deposit': '',
    'area': '',
    "airport": "",
    "bus_station": "",
    "train_station": "",
    "subway_station": "",
    "customLocality": "",
    "hospital": "",
    "gas_station": "",
    "atm": "",
    "school": "",
    "movie_theater": "",
    "shopping_mall": "",
    "grocery_or_supermarket": "",
    "pharmacy": "",
    'bedroom': '',
    'tenantType': '',
    'availableFrom': '',
    'parkingType': '',
    'propertyAge': '',
    'balconyCount': '',
    'type': '',
    'ava': [],
    'notava': []
}

# Online Resource
URL = "https://www.nobroker.in/property/rent/bangalore/Bangalore/?" \
      "searchParam=W3sibGF0IjoxMi45NzE1OTg3LCJsb24iOjc3LjU5NDU2MjcsInBs" \
      "YWNlSWQiOiJDaElKYlU2MHlYQVdyanNSNEU5LVVlakQzX2ciLCJwbGFjZU5hbWUiOiJCYW5nYWxvcmUifV0=" \
      "&sharedAccomodation=0&orderBy=nbRank,desc&radius=2&traffic=true&travelTime=30&propertyType=rent" \
      "&pageNo="


# Make BS OBJECT
def source(URL, query, Parser):
    src = request.urlopen(URL + query)  # URL QUERY
    src = BeautifulSoup(src, Parser)  # BS OBJECT
    return src  # Output


# Cleaning HTML File
def transform(html):
    soup = html  # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)
    # returning transformed text
    return str(text.encode(encoding='utf_8', errors='ignore'))


def main(n):
    for i in range(1, n + 1):
        s = source(URL, str(i), 'html5lib')

        for i in s.find_all('div', {"class": "card"}):
            temp = raw.copy()
            # desc
            temp['dump'] = transform(i)

            for b in i.find_all('a', {"class": "card-link-detail"}):

                temp['link'] = b['href']
                o = source(b['href'], '', 'html5lib')

                # overview
                for j in o.find_all('div', {"class": "text-align-center rentMaintDiv"}):  # ava
                    temp['rent'] = transform(j)

                for j in o.find_all('h1', {"class": "detail-title-main"}):  # ava
                    temp['title'] = transform(j)

                for j in o.find_all('h5', {"class": "margin-top-bottom-0"}):  # ava
                    temp['subtitle'] = j['title']

                for j in o.find_all('div', {
                    "class": "bedroomCount col-sm-6 col-xs-6 solid-border-right text-align-left"}):  # ava
                    temp['bedroom'] = transform(j)

                for j in o.find_all('div', {"class": "flatsCount col-sm-6 col-xs-6 text-align-left"}):  # ava
                    temp['type'] = transform(j)

                for j in o.find_all('div', {"class": "propertyAge col-sm-6 col-xs-6 text-align-left"}):  # ava
                    temp['propertyAge'] = transform(j)

                for j in o.find_all('div', {
                    "class": "tenantType col-sm-6 col-xs-6 solid-border-right text-align-left"}):  # ava
                    temp['tenantType'] = transform(j)

                for j in o.find_all('div', {
                    "class": "balconyCount col-sm-6 col-xs-6 solid-border-right text-align-left"}):  # ava
                    temp['balconyCount'] = transform(j)

                for j in o.find_all('div', {"class": "availableFrom col-sm-6 col-xs-6 text-align-left"}):  # ava
                    temp['availableFrom'] = transform(j)

                for j in o.find_all('div', {"class": "availableFrom col-sm-6 col-xs-6 text-align-left"}):  # ava
                    temp['availableFrom'] = transform(j)

                for j in o.find_all('div', {
                    "class": "parkingType col-sm-6 col-xs-6 solid-border-right text-align-left"}):  # ava
                    temp['parkingType'] = transform(j)

                for j in o.find_all('div', {"itemprop": "valueReference"}):  # ava
                    temp['deposit'] = transform(j)

                for j in o.find_all('div', {"class": "col-xs-2 col-sm-2 solid-border-right"}):  # ava
                    if transform(j).find('Sq.Ft') != -1:
                        temp['area'] = temp['area'] + transform(j)

                # overview
                for j in o.find_all('div',
                                    {"style": "background-color:white;margin-top:10px;padding-bottom: 15px"}):  # ava
                    temp['overview'] = transform(j)

                e = list()
                # faclity
                for j in o.find_all('div', {"class": "amenities-text col-sm-10 col-xs-9"}):  # ava
                    e.append(j.getText())
                temp['ava'] = e.copy()

                e = list()
                for j in o.find_all('div', {"class": "amenities-text col-sm-10 col-xs-9 light"}):  # not ava
                    e.append(j.getText())
                temp['notava'] = e.copy()

            l.append(temp)
            break

    with open('raw.json', 'w') as f:
        f.write(dumps(l, indent=4))

    print(dumps(l, indent=4))


# if __name__ == "__main__":
#     main(1)  # n = no of iteration max u want

from requests_html import HTMLSession

session = HTMLSession()

r = session.get("https://www.nobroker.in/property/3-BHK-apartment-for-rent-in-Kudlu-Gate-bangalore-for-rs-35000/ff8081816cef3baf016cf027dc2316fb/detail")
r.html.render()

print(r.text)