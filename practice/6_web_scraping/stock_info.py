"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""

from genericpath import exists
from bs4 import BeautifulSoup, NavigableString, Tag
from numpy import sort
import requests




url = "https://finance.yahoo.com/most-active"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
countries = ['AFGHANISTAN', 'ALAND ISLANDS', 'ALBANIA', 'ALGERIA', 'AMERICAN SAMOA', 'ANDORRA', 'ANGOLA', 'ANGUILLA', 'ANTARCTICA', 'ANTIGUA AND BARBUDA', 'ARGENTINA', 'ARMENIA', 'ARUBA', 'AUSTRALIA', 'AUSTRIA', 'AZERBAIJAN', 'BAHAMAS', 'BAHRAIN', 'BANGLADESH', 'BARBADOS', 'BELARUS', 'BELGIUM', 'BELIZE', 'BENIN', 'BERMUDA', 'BHUTAN', 'BOLIVIA, PLURINATIONAL STATE OF', 'BONAIRE, SINT EUSTATIUS AND SABA', 'BOSNIA AND HERZEGOVINA', 'BOTSWANA', 'BOUVET ISLAND', 'BRAZIL', 'BRITISH INDIAN OCEAN TERRITORY', 'BRUNEI DARUSSALAM', 'BULGARIA', 'BURKINA FASO', 'BURUNDI', 'CAMBODIA', 'CAMEROON', 'CANADA', 'CAPE VERDE', 'CAYMAN ISLANDS', 'CENTRAL AFRICAN REPUBLIC', 'CHAD', 'CHILE', 'CHINA', 'CHRISTMAS ISLAND', 'COCOS (KEELING) ISLANDS', 'COLOMBIA', 'COMOROS', 'CONGO', 'CONGO, THE DEMOCRATIC REPUBLIC OF THE', 'COOK ISLANDS', 'COSTA RICA', "CÔTE D'IVOIRE", 'CROATIA', 'CUBA', 'CURAÇAO', 'CYPRUS', 'CZECH REPUBLIC', 'DENMARK', 'DJIBOUTI', 'DOMINICA', 'DOMINICAN REPUBLIC', 'ECUADOR', 'EGYPT', 'EL SALVADOR', 'EQUATORIAL GUINEA', 'ERITREA', 'ESTONIA', 'ETHIOPIA', 'FALKLAND ISLANDS (MALVINAS)', 'FAROE ISLANDS', 'FIJI', 'FINLAND', 'FRANCE', 'FRENCH GUIANA', 'FRENCH POLYNESIA', 'FRENCH SOUTHERN TERRITORIES', 'GABON', 'GAMBIA', 'GEORGIA', 'GERMANY', 'GHANA', 'GIBRALTAR', 'GREECE', 'GREENLAND', 'GRENADA', 'GUADELOUPE', 'GUAM', 'GUATEMALA', 'GUERNSEY', 'GUINEA', 'GUINEA-BISSAU', 'GUYANA', 'HAITI', 'HEARD ISLAND AND MCDONALD ISLANDS', 'HOLY SEE (VATICAN CITY STATE)', 'HONDURAS', 'HONG KONG', 'HUNGARY', 'ICELAND', 'INDIA', 'INDONESIA', 'IRAN, ISLAMIC REPUBLIC OF', 'IRAQ', 'IRELAND', 'ISLE OF MAN', 'ISRAEL', 'ITALY', 'JAMAICA', 'JAPAN', 'JERSEY', 'JORDAN', 'KAZAKHSTAN', 'KENYA', 'KIRIBATI', "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF", 'KOREA, REPUBLIC OF', 'KUWAIT', 'KYRGYZSTAN', "LAO PEOPLE'S DEMOCRATIC REPUBLIC", 'LATVIA', 'LEBANON', 'LESOTHO', 'LIBERIA', 'LIBYA', 'LIECHTENSTEIN', 'LITHUANIA', 'LUXEMBOURG', 'MACAO', 'MACEDONIA, REPUBLIC OF', 'MADAGASCAR', 'MALAWI', 'MALAYSIA', 'MALDIVES', 'MALI', 'MALTA', 'MARSHALL ISLANDS', 'MARTINIQUE', 'MAURITANIA', 'MAURITIUS', 'MAYOTTE', 'MEXICO', 'MICRONESIA, FEDERATED STATES OF', 'MOLDOVA, REPUBLIC OF', 'MONACO', 'MONGOLIA', 'MONTENEGRO', 'MONTSERRAT', 'MOROCCO', 'MOZAMBIQUE', 'MYANMAR', 'NAMIBIA', 'NAURU', 'NEPAL', 'NETHERLANDS', 'NEW CALEDONIA', 'NEW ZEALAND', 'NICARAGUA', 'NIGER', 'NIGERIA', 'NIUE', 'NORFOLK ISLAND', 'NORTHERN MARIANA ISLANDS', 'NORWAY', 'OMAN', 'PAKISTAN', 'PALAU', 'PALESTINIAN TERRITORY, OCCUPIED', 'PANAMA', 'PAPUA NEW GUINEA', 'PARAGUAY', 'PERU', 'PHILIPPINES', 'PITCAIRN', 'POLAND', 'PORTUGAL', 'PUERTO RICO', 'QATAR', 'RÉUNION', 'ROMANIA', 'RUSSIAN FEDERATION', 'RWANDA', 'SAINT BARTHÉLEMY', 'SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA', 'SAINT KITTS AND NEVIS', 'SAINT LUCIA', 'SAINT MARTIN (FRENCH PART)', 'SAINT PIERRE AND MIQUELON', 'SAINT VINCENT AND THE GRENADINES', 'SAMOA', 'SAN MARINO', 'SAO TOME AND PRINCIPE', 'SAUDI ARABIA', 'SENEGAL', 'SERBIA', 'SEYCHELLES', 'SIERRA LEONE', 'SINGAPORE', 'SINT MAARTEN (DUTCH PART)', 'SLOVAKIA', 'SLOVENIA', 'SOLOMON ISLANDS', 'SOMALIA', 'SOUTH AFRICA', 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS', 'SPAIN', 'SRI LANKA', 'SUDAN', 'SURINAME', 'SOUTH SUDAN', 'SVALBARD AND JAN MAYEN', 'SWAZILAND', 'SWEDEN', 'SWITZERLAND', 'SYRIAN ARAB REPUBLIC', 'TAIWAN, PROVINCE OF CHINA', 'TAJIKISTAN', 'TANZANIA, UNITED REPUBLIC OF', 'THAILAND', 'TIMOR-LESTE', 'TOGO', 'TOKELAU', 'TONGA', 'TRINIDAD AND TOBAGO', 'TUNISIA', 'TURKEY', 'TURKMENISTAN', 'TURKS AND CAICOS ISLANDS', 'TUVALU', 'UGANDA', 'UKRAINE', 'UNITED ARAB EMIRATES', 'UNITED KINGDOM', 'UNITED STATES', 'UNITED STATES MINOR OUTLYING ISLANDS', 'URUGUAY', 'UZBEKISTAN', 'VANUATU', 'VENEZUELA, BOLIVARIAN REPUBLIC OF', 'VIET NAM', 'VIRGIN ISLANDS, BRITISH', 'VIRGIN ISLANDS, U.S.', 'WALLIS AND FUTUNA', 'YEMEN', 'ZAMBIA', 'ZIMBABWE']
stocks_info = {}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}





################################################ Stock Info ################################################

# Find all tables that contain Stocks data (CODE, NAME & link to profile)
code_tables = soup.find_all("a", class_="Fw(600) C($linkColor)")
index = 0
for column in code_tables:
    stocks_info.update({index: {'Name': 'tbd', 'Code': column.text, 'Country': 'tbd', 'Employees': 0, 'CEO': 'tbd', 'Year born': 0, '52-Week-Change': 0, 'Total-Cash': 0}})
    index += 1

# Find table that contain stock info
table = soup.find_all("tbody")
messy_helper = []
clean_helper = []

#We get the strings inside the table 
for item in table:
    for i in item.strings:
        messy_helper.append(i)
        
#We clean the strings and get the info we need
for i in range(0, len(messy_helper), 9):
    clean_helper.extend(messy_helper[i:i+2])

#Compare between our stocks_info dict code and the clean_helper code if they are the same we update the stocks_info name to the clean_helper name
for i in range(0, len(clean_helper), 2):
    for key, value in stocks_info.items():
        if stocks_info[key]['Code'] == clean_helper[i]: 
            stocks_info[key]['Name'] = clean_helper[i+1]

# Find all links to profile
profile_links = soup.find_all("a", href=True)
href = []
for table in code_tables:
    href.append(table['href'])

################################################ Company info ################################################
country = []
actual_employees = []
profile_href = []
statistics_href = []
holders_href = []

# Find Strings inside <p> tags
print('------------------------ Start - Collection of data from Stocks ------------------------')
for link in href:
    print(('https://finance.yahoo.com'+link))
    # Make request to link
    company_page = requests.get('https://finance.yahoo.com'+link)
    company_soup = BeautifulSoup(company_page.content, 'html.parser')
    
    # Get country
    profile_content = company_soup.find('p', class_="D(ib) W(47.727%) Pend(40px)").strings
    for strings in profile_content:
        if strings.upper() in countries:
            country.append(strings)
            
    # Get employees
    employes_tag_p = company_soup.find('p', class_='D(ib) Va(t)')
    span = employes_tag_p.find_all('span', class_='Fw(600)')
    actual_employees.append(span[2].text)
    
    
    #Get href to profile
    nav_div = [item for item in company_soup.find_all('li', attrs={'data-test' : True})]
    for item in nav_div:
        if item['data-test'] == 'COMPANY_PROFILE':
            profile_href.append(item.a['href'])
        if item['data-test'] == 'STATISTICS':
            statistics_href.append(item.a['href'])
        if item['data-test'] == 'HOLDERS':
            holders_href.append(item.a['href'])
    
print('------------------------ End - Collection of data from Stocks -------------------------')
    
    

#Place countries inside stocks_info dict
for key, value in stocks_info.items():
    for i in range(len(country)):
        stocks_info[i]['Country'] = country[i]
        i += 1


#Place employees inside stocks_info dict
for key, value in stocks_info.items():
    for i in range(len(actual_employees)):
        stocks_info[i]['Employees'] = actual_employees[i]
        i += 1




################################################ CEO info ################################################
messy_ceo_info = []
executives = []
index = 0
print('--------------------------- Start - Getting stock information --------------------------')
for link in profile_href:
    print('https://finance.yahoo.com'+link)
    profile_page = requests.get('https://finance.yahoo.com'+link, headers=headers)
    profile_soup = BeautifulSoup(profile_page.content, 'html.parser')
    
    # Get CEO
    tr = profile_soup.find_all("tr", class_="C($primaryColor) BdB Bdc($seperatorColor) H(36px)")
    td = profile_soup.find_all("td", class_="Ta(start)")
    
        
    #Collect CEO name and junk
    for element in tr:
        if element.text.find('CEO') != -1:
            messy_ceo_info.append(element.text)
        else: 
            pass

    # Appending Elements to executives list
    for element in td:
        executives.append(element.text)
    
    
print('--------------------------- End - Getting stock information --------------------------')


   
#Appending CEO year born to dict
year_born = []
dict_key = 0
for elem in messy_ceo_info:
    year = elem[-4:]
    if year.isdigit():
        stocks_info[dict_key]['Year born'] = year
    else:
        pass
    dict_key+=1

# print(stocks_info)
def print_dict(ceo_dict: dict):

    name_length = 0
    code_length = 0
    country_length = 0
    employees_length = 0
    ceo_length = 0
    totalcash_length = 0

    #Calculate max length of each column
    for key, value in ceo_dict.items():
        if ceo_dict[key]['Name'].__len__() > name_length:
            name_length = ceo_dict[key]['Name'].__len__()
        if ceo_dict[key]['Code'].__len__() > code_length:
            code_length = ceo_dict[key]['Code'].__len__()
        if ceo_dict[key]['Country'].__len__() > country_length:
            country_length = ceo_dict[key]['Country'].__len__()
        if ceo_dict[key]['Employees'].__len__() > employees_length:
            employees_length = ceo_dict[key]['Employees'].__len__()
        if ceo_dict[key]['CEO'].__len__() > ceo_length:
            ceo_length = ceo_dict[key]['CEO'].__len__()
        if ceo_dict[key]['Total-Cash'].__len__() > totalcash_length:
            totalcash_length = ceo_dict[key]['Total-Cash'].__len__()
    overall_length = name_length + code_length + country_length + employees_length + ceo_length + 30
    ############################################### Print 10 youngest ceo ###################################################################
    #Print header
    print('='*(round((overall_length-34)/2)-1)+' 5 stocks with most youngest CEOs '+'='*46)
    #Print column names
    print('| Name'+' '*(name_length-5)+'| Code'+' '*(code_length-4)+' | Country'+' '*(country_length-6)+' | Employees'+' '*(employees_length-9)+' | CEO Name'+' '*(ceo_length-8)+'| CEO Year Born |')
    #Print bottom border
    print('-'*overall_length)
    #Print data
    print('\n')
    sorted_yearborn = sorted(ceo_dict.items(), key=lambda x: x[1]['Year born'], reverse=True)
    for key, value in sorted_yearborn[:5]:
        print('|'+value['Name']+' '*(name_length-value['Name'].__len__())+'| '+value['Code']+' '*(code_length-value['Code'].__len__())+' | '+value['Country']+' '*(country_length-value['Country'].__len__())+' | '+value['Employees']+' '*(employees_length-value['Employees'].__len__())+' | '+value['CEO']+' '*(ceo_length-value['CEO'].__len__())+' | '+value['Year born']+' '*10+'|')
   
    # for item in ceo_dict.values():
    #     print('|'+item['Name']+' '*(name_length-item['Name'].__len__())+'| '+item['Code']+' '*(code_length-item['Code'].__len__())+' | '+item['Country']+' '*(country_length-item['Country'].__len__())+' | '+item['Employees']+' '*(employees_length-item['Employees'].__len__())+' | '+item['CEO']+' '*(ceo_length-item['CEO'].__len__())+' | '+item['Year born']+' '*10+'|')
        
    print('\n')
    ###################################### Print 10 stocks with best 52-Week Change. ########################################################
    #Print header
    print('='*24+' 10 stocks with best 52-Week Change. '+'='*24)
    #Print column names
    print('| Name'+' '*(name_length-5)+'| Code | 52-Week Change       |   Total Cash   |')
    #Print bottom borders
    print('-------------------------------------------------------------------------------------')
    for item in ceo_dict.values():
        if item['Total-Cash'].__len__() == 7:
            print('|'+item['Name']+' '*(name_length-item['Name'].__len__())+'| '+item['Code']+' '*(code_length-item['Code'].__len__())+' | '+str(item['52-Week-Change'])+' '*18+'| '+str(item['Total-Cash'])+' '*8+'|')
        elif item['Total-Cash'].__len__() == 6:
            print('|'+item['Name']+' '*(name_length-item['Name'].__len__())+'| '+item['Code']+' '*(code_length-item['Code'].__len__())+' | '+str(item['52-Week-Change'])+' '*18+'| '+str(item['Total-Cash'])+' '*9+'|')
        elif item['Total-Cash'].__len__() == 5:
            print('|'+item['Name']+' '*(name_length-item['Name'].__len__())+'| '+item['Code']+' '*(code_length-item['Code'].__len__())+' | '+str(item['52-Week-Change'])+' '*18+'| '+str(item['Total-Cash'])+' '*10+'|')
        elif item['Total-Cash'].__len__() == 4:
            print('|'+item['Name']+' '*(name_length-item['Name'].__len__())+'| '+item['Code']+' '*(code_length-item['Code'].__len__())+' | '+str(item['52-Week-Change'])+' '*18+'| '+str(item['Total-Cash'])+' '*11+'|')
        elif item['Total-Cash'].__len__() == 3:
            print('|'+item['Name']+' '*(name_length-item['Name'].__len__())+'| '+item['Code']+' '*(code_length-item['Code'].__len__())+' | '+str(item['52-Week-Change'])+' '*18+'| '+str(item['Total-Cash'])+' '*12+'|')
        elif item['Total-Cash'].__len__() == 2:
            print('|'+item['Name']+' '*(name_length-item['Name'].__len__())+'| '+item['Code']+' '*(code_length-item['Code'].__len__())+' | '+str(item['52-Week-Change'])+' '*18+'| '+str(item['Total-Cash'])+' '*13+'|')

 


key = 0
flag = True
for index in range(len(executives)):
    if executives[index].find('CEO') != -1:
        if executives[index].find('Co-CEO') != -1:
            if flag == True:
                stocks_info[key]['CEO'] = executives[index-1]
                key += 1
                flag = False
            else:
                pass
        else:
            stocks_info[key]['CEO'] = executives[index-1]
            key += 1

##############################################################################################################
'''
https://finance.yahoo.com/most-active
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
=============== 10 stocks with best 52-Week Change. ==========
| Name        | Code | 52-Week Change       |   Total Cash   |
--------------------------------------------------------------
| Pfizer Inc. | PFE  |               |           |           |
'''    
print('--------- Start - 10 stocks with best 52-Week Change. ----------')
clean_cash = []
clean_week = []
for link in statistics_href:
    if link.find('ENIA') != -1:
        link = '/quote/ENIAY/key-statistics?p=ENIAY'
    statistics_page = requests.get('https://finance.yahoo.com'+link, headers=headers)
    statistics_soup = BeautifulSoup(statistics_page.content, 'html.parser')
    print('https://finance.yahoo.com'+link)

    # Get 52-Week Change
    tr = statistics_soup.find_all("tr", class_="Bxz(bb) H(36px) BdB Bdbc($seperatorColor)")
    cash_tr = statistics_soup.find_all("tr", class_="Bxz(bb) H(36px) BdY Bdc($seperatorColor)")
    percentage = tr[1].text.split(' ')[3]
    total_cash = cash_tr[7].text.rsplit(' ')[2]

    clean_week.append(percentage[1:])
    clean_cash.append(total_cash[5:])
    # else:
    #     pass

    

index = 0
for item in stocks_info:
    stocks_info[index]['52-Week-Change'] = clean_week[index]
    stocks_info[index]['Total-Cash'] = clean_cash[index]
    index += 1
print('---------- End - 10 stocks with best 52-Week Change. ----------')
    


##############################################################################################################
def print_blackrock(holds_dict: dict):
    name_length = 0
    shares_length = 0
    date_length = 0
    out_length = 0
    value_length = 0
    code_length = 0

    for key in holds_dict:
        for i in range(len(stocks_info)):
            if key in stocks_info[i]['Code']:
                holds_dict[key]['Name'] = stocks_info[i]['Name']
            
    for key, value in holds_dict.items():
        if holds_dict[key]['Name'].__len__() > name_length:
            name_length = holds_dict[key]['Name'].__len__()
        if holds_dict[key]['Shares'].__len__() > shares_length:
            shares_length = holds_dict[key]['Shares'].__len__()
        if holds_dict[key]['Date_Reported'].__len__() > date_length:
            date_length = holds_dict[key]['Date_Reported'].__len__()
        if holds_dict[key]['Out'].__len__() > out_length:
            out_length = holds_dict[key]['Out'].__len__()
        if holds_dict[key]['Value'].__len__() > value_length:
            value_length = holds_dict[key]['Value'].__len__()
        if holds_dict[key]['Code'].__len__() > code_length:
            code_length = holds_dict[key]['Code'].__len__()
    
    
    overall_length = name_length + shares_length + date_length + out_length + value_length + code_length

    print('='*37+' 10 largest holds of Blackrock Inc. '+'='*28)
    print('| Name'+' '*(name_length-5)+'| Code | Shares        | Date Reported | %_Out | Value'+' '*10+'|')
    print('-'*(overall_length+16))
    sorted_l = {k: v for k, v in sorted(holds_dict.items(), key=lambda item: item[1]['Value'], reverse=True)}
    for key, value in [*sorted_l.items()][:10]:
        print('|'+value['Name']+' '*(name_length-value['Name'].__len__())+'| '+value['Code']+' '*(code_length-value['Code'].__len__())+' | '+value['Shares']+' '*(shares_length-value['Shares'].__len__())+' | '+value['Date_Reported']+' '*(date_length-value['Date_Reported'].__len__())+'  | '+value['Out']+' '*(out_length-value['Out'].__len__())+'| '+value['Value']+' '*(value_length-value['Value'].__len__())+'|')
    

messy_holder = []
td_helper = []
stocks = {}
'''
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, %_Out, Value.
    All fields except first two should be taken from Holders tab.

================== 10 largest holds of Blackrock Inc. ==================
| Name        | Code | Shares        | Date Reported   | %_Out | Value |
------------------------------------------------------------------------
| Pfizer Inc. | PFE  |               |                 |       |       |

'''
print('---------------------- Start - 10 largest holds of Blackrock Inc. ----------------------')
for link in holders_href:
    print(('https://finance.yahoo.com'+link))
    holders_page = requests.get('https://finance.yahoo.com'+link, headers=headers)
    holders_soup = BeautifulSoup(holders_page.content, 'html.parser')
    tr = holders_soup.find_all("tr", class_="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)")
    code = link.split('/')[2]

    for index in range(len(tr)):
        if tr[index].text.find('Blackrock') != -1:
            td_helper.append(tr[index].find_all('td'))

    for list in td_helper:
        stocks[code] = {'Shares': list[1].text, 'Date_Reported': list[2].text, 'Out': list[3].text, 'Value': list[4].text, 'Code': code}
print('---------------------- End - 10 largest holds of Blackrock Inc. ----------------------')

print_dict(stocks_info)