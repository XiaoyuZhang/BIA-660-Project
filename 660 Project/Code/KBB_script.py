from bs4 import BeautifulSoup
import time
from selenium import webdriver
import os

def run(zipcode):
    def print2csv(html):      ###some highlight cell will be missing, see wagon's first page's fisrt element   （about 80%）
        soup = BeautifulSoup(html,'lxml')

        cars = soup.findAll('div', {'class':"listing js-used-listing"})

        for car in cars:
            name = car.find('a', {'class':"js-vehicle-name"}) or 'NA'
            if name != 'NA': name = name.string.strip().replace(',','')

            price = car.find('span', {'class':"title-four highlight"}) or 'NA'
            if price != 'NA': price = price.string.strip().replace(',','').replace('$','')

            mei = car.find('div', {'class':"text-content"}).findAll('p', {'class':"paragraph-two"})
            mei_contents = {'Mileage':'NA', 'Exterior':'NA', 'Interior':'NA'}
            for i, j in enumerate(mei):
                if ':' in j.string:
                    part1, part2 = j.string.split(':', 1)
                    mei_contents[part1] = part2.strip().replace(',','')
            mileage, exterior, interior = mei_contents['Mileage'], mei_contents['Exterior'], mei_contents['Interior']

            dealer_name = car.find('p', {'class':"paragraph-two dealer-name "}) or 'NA'
            if dealer_name != 'NA': dealer_name = dealer_name.string.replace(',','')

            ted = car.find('div', {'class':"inner-column specs-right"}).findAll('p', {'class':"paragraph-two"})
            ted_contents = {'Trans.':'NA', 'Engine':'NA', 'Doors':'NA'}
            for i, j in enumerate(ted):
                part1, part2 = j.string.split(':', 1)
                ted_contents[part1] = part2.strip().replace(',','')
            trans, engine, doors =ted_contents['Trans.'], ted_contents['Engine'], ted_contents['Doors']

            photos = car.find('span', {'class':"photos js-quick-view js-quick-view-photos"}) or 'NA'
            if photos != 'NA': photos = photos.find('span').string.replace(',','')

            videos = car.find('span', {'class':"videos js-quick-view js-quick-view-videos"}) or 'NA'
            if videos != 'NA': videos = videos.find('span').string.replace(',','')

            for i in [name, price, mileage, exterior, interior, dealer_name, trans, engine, doors, photos, videos]:
                csvfile.write(i)
                csvfile.write(',')
            csvfile.write(moto_type)
            csvfile.write('\n')

    path = '/Users/zhangxiaoyu/Desktop/datasets'
    driver = webdriver.Chrome(os.path.join(path, './chromedriver'))
    csvfile = open(os.path.join(path, '%s.csv'%zipcode), 'w', encoding='utf-8')

    for moto_type in ['sedan', 'wagon', 'suv', 'coupe', 'hatch', 'convert', 'trucks', 'vans']: ###get 1000 in every type of moto
        end = 10
        for i in range(1, 11): ## we assume we have 10 pages initially
            if i > end: break
            url = 'https://www.kbb.com/cars-for-sale/cars/?distance=75&bodystyle=' + \
                   moto_type + '&p=' + str(i) + '&nr=100&s=kbbrank'
            driver.get(url)
            if (i == 1) and (moto_type == 'sedan'):
                element = driver.find_element_by_id("selectedZipCode")
                element.send_keys(zipcode)

                element = driver.find_element_by_id("enterzipsubmit")
                webdriver.common.action_chains.ActionChains(driver).click(on_element=element).perform()
                time.sleep(3)
            if (i == 1):
                try:
                    end = int(driver.find_element_by_class_name("pages").get_attribute('innerHTML').replace('>', '<').split('<')[6])
                    print(moto_type, 'has', end, 'pages when zip code is %s'%zipcode)
                except:
                    end = 1
                    print(moto_type, 'only has', end, 'page when zip code is %s'%zipcode)
            html = driver.page_source
            print2csv(html)
            print('page', i, 'completed!')
            time.sleep(1)
    print('zipcode %s'%zipcode, ' DONE!!!!!!!!!!!!!!!')
    csvfile.close()
    driver.quit()

if __name__=='__main__':
    for _ in ['96817']:
        print('##########################################')
        run(_)
