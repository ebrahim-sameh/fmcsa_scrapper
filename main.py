import csv

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

onepage = 0
pagestoscrape = 0
lntxt = 'a'
pages = 999999999999999
schema = ['USDOT Number', 'Prefix', 'Docket Number', 'Legal Name', 'DBA Name', 'City', 'State', 'Zip code',
          'Fax number', 'Business Address', 'Business Telephone'
    , 'Mail Address', 'Mail Telephone and Fax', 'Undeliverable Mail','Common Authority Status', 'contract Authority Status', 'broker Authority Status','common Application Pending','contract Application Pending','broker Application Pending',
          'Property','Passenger','Household Goods','Private','Enterprise',
          'Type', 'Insurance Carrier', 'Policy/Surety', 'Posted Date', 'Coverage From', 'Coverage to', 'Effective Date',
          'Cancellation Date',
          'Type', 'Insurance Carrier', 'Policy/Surety', 'Posted Date', 'Coverage From', 'Coverage to', 'Effective Date',
          'Cancellation Date'
          ]
site = "https://li-public.fmcsa.dot.gov/LIVIEW/pkg_menu.prc_menu"
path = 'chromedriver'
# chrome_options = Options()
# chrome_options.add_extension('extension_8_2_3_0.crx')
#
driver = webdriver.Chrome(path)
# driver.get('chrome://extensions/')
driver.get(site)
driver.implicitly_wait(10)
# driver.maximize_window()
grbf = Select(driver.find_element(By.ID, 'menu'))
grbf.select_by_value('CARR_SEARCH')
gobtn = driver.find_element(By.XPATH, '/html/body/font/table[1]/tbody/tr/td/div/div/table/tbody/tr/td/form/input[1]')
gobtn.click()
legalname = driver.find_element(By.XPATH, '//*[@id="legal_name"]')
legalname.send_keys(lntxt)
WebDriverWait(driver, 100).until(
    EC.invisibility_of_element_located((By.XPATH, "/html/body/font/center[1]/form/table[3]/tbody/tr/td")))
# print('waited for captcha check and now scarping..')
# table = driver.find_element(By.CSS_SELECTOR, "body > font > table:nth-child(5)")
# with open('eggs.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for row in table.find_elements(By.CSS_SELECTOR,'tr'):
#         wr.writerow([d.text for d in row.find_elements(By.CSS_SELECTOR,'td')])

table = driver.find_element(By.CSS_SELECTOR, "body > font > table:nth-child(5)")
prospects = table.find_elements(By.CSS_SELECTOR, 'td')
datalist = []
listdatalist = []

r = 2
while (1):
    try:
        try:
            tablerow = driver.find_element(By.XPATH, '/html/body/font/table[2]/tbody/tr[' + str(r) + ']')
            rowprospects = tablerow.find_elements(By.CSS_SELECTOR, 'td')
            # for p in rowprospects:
            #     tempdatalist={'dot_number' : rowprospects[p].text,
            #               'prefix': rowprospects[p].text,
            #               'docket_number': rowprospects[p].text,
            #               'dba_name': rowprospects[p].text,
            #               'city': rowprospects[p].text,
            #               'state': rowprospects[p].text,
            #               }
            #     datalist.append(tempdatalist)
            for element in rowprospects:
                datalist.append(element.text)
            datalist.append('')

                # print('oneprint')
            htmls = driver.find_element(By.XPATH,
                                        '/html/body/font/table[2]/tbody/tr[' + str(r) + ']/td[8]/center/font/form')
            htmls.click()
            # print('opened html and scraping phone and adress from here')
            try:
                elem = driver.find_element(By.XPATH, '/html/body/font/table[4]/tbody/tr/td/font/b')
                phonetable = driver.find_element(By.XPATH, '/html/body/font/table[6]')
                activeinsurancetavle = driver.find_element(By.XPATH,'/html/body/font/table[7]')
                propertytable = driver.find_element(By.XPATH,'/html/body/font/table[8]')
                # print('tableeee6')
            except NoSuchElementException:
                phonetable = driver.find_element(By.XPATH, '/html/body/font/table[5]')
                # print('tableeee5')
                activeinsurancetavle = driver.find_element(By.XPATH,'/html/body/font/table[6]')
                propertytable = driver.find_element(By.XPATH,'/html/body/font/table[7]')
            # def check_exists_by_xpath():
            #     try:
            #         driver.find_element(By.LINK_TEXT, 'This entity has a pending insurance cancellation.')
            #     except NoSuchElementException:
            #         return False
            #     return True
            # if not check_exists_by_xpath:
            #     phonetable = driver.find_element(By.XPATH, '/html/body/font/table[6]')
            #     print('tableeee6')
            # else:
            #     phonetable = driver.find_element(By.XPATH, '/html/body/font/table[5]')
            #     print('tableeee5')
            rowphone = phonetable.find_elements(By.CSS_SELECTOR, 'td')
            rowactive = activeinsurancetavle.find_elements(By.CSS_SELECTOR,'td')
            rowprop = propertytable.find_elements(By.CSS_SELECTOR,'td')
            for element in rowphone:
                datalist.append(element.text)
            for element in rowactive:
                datalist.append(element.text)
            for element in rowprop:
                datalist.append(element.text)
            insactv = driver.find_element(By.XPATH, '/html/body/font/center[1]/table/tbody/tr/td[1]/form')
            insactv.click()
            # print('showing active and pending insurance and scrape here')
            instable = driver.find_element(By.XPATH, '/html/body/font/table[4]')
            rowins = instable.find_elements(By.CSS_SELECTOR, 'td')
            for element in rowins:
                datalist.append(element.text)
            listdatalist.append(datalist)
            print('one prospect scrapped completley!')
            print(listdatalist)
            datalist = []
            driver.back()
            # print('back to html')
            driver.back()
            # print('back to 10 recs')
            # print(r)
            r = r + 1
        except NoSuchElementException:
            if pages == 0:
                elem = driver.find_element(By.XPATH, '/html/body/font/center[2]/table/tbody/tr/td/form/input[10]')
                elem.click()
                pages = pages + 1
                r = 2
                print('next 10 on first page')
                continue
            elif pages > 0 and pages <= pagestoscrape:
                elem = driver.find_element(By.XPATH, '/html/body/font/center[2]/table/tbody/tr/td[2]/form/input[10]')
                elem.click()
                pages = pages + 1
                r = 2
                print('next 10 recs on page')
                continue
            else:
                break
            # try:
            #     elem = driver.find_element(By.XPATH, '/html/body/font/center[2]/table/tbody/tr/td/form/input[10]')
            #     elem.click()
            #     print('next 10 recs on frst page')
            #     pages = pages+1
            #     continue
            # except NoSuchElementException:
            #     elem = driver.find_element(By.XPATH, '/html/body/font/center[2]/table/tbody/tr/td[2]/form/input[10]')
            #     elem.click()
            #     print('next 10 recs on other pages')
            #     pages = pages+1
            #     continue
            break
    except WebDriverException:
        tot = 0
        for lst in listdatalist:
            lns = len(listdatalist[tot])
            if lns > 9:
                adrs = listdatalist[tot][9]
                adrslns = length = len(adrs)
                adrsremove = len(listdatalist[tot][5]) + len(listdatalist[tot][6]) +7
                f = adrslns - adrsremove
                listdatalist[tot][9] = adrs[:f]
                fax = listdatalist[tot][10]
                faxlns = len(listdatalist[tot][10])
                zipcode = adrs[adrslns - 5:]
                listdatalist[tot][7] = zipcode
                if faxlns > 15:
                    phoneandfax = listdatalist[tot][10]
                    listdatalist[tot][10] = phoneandfax[:14].removesuffix('Fa')
                    adrslns = length = len(adrs)
                    faxnum = fax[faxlns - 15:]
                    listdatalist[tot][8] = faxnum.removeprefix('Fax:')
                tot = tot + 1
            else:
                tot = tot + 1
        with open("Data_output.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([g for g in schema])
            writer.writerows(listdatalist)
            onepage = 1
            break
if onepage < 1:
    tot = 0
    for lst in listdatalist:
        lns = len(listdatalist[tot])
        if lns > 9:
            adrs = listdatalist[tot][9]
            adrslns = length = len(adrs)
            adrsremove = len(listdatalist[tot][5]) + len(listdatalist[tot][6]) + 7
            f = adrslns - adrsremove
            listdatalist[tot][9] = adrs[:f]
            fax = listdatalist[tot][10]
            faxlns = len(listdatalist[tot][10])
            zipcode = adrs[adrslns - 5:]
            listdatalist[tot][7] = zipcode
            if faxlns > 15:
                phoneandfax = listdatalist[tot][10]
                listdatalist[tot][10] = phoneandfax[:14].removesuffix('Fa')
                adrslns = length = len(adrs)
                faxnum = fax[faxlns - 15:]
                listdatalist[tot][8] = faxnum.removeprefix('Fax:')
            tot = tot + 1
        else:
            tot = tot + 1
    with open("Data_output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([g for g in schema])
        writer.writerows(listdatalist)
        onepage = 1
# for prospect in prospects:
#     # print(prospect.text)
#     print('done')
