# Packages
from RPA.Browser.Selenium import Selenium
from modulos import constants


# Function that setup configs to scrapping individual investment table
def setup_individual_investment_table():
    try:
        # Wait to load the individual investment and select 'All' itens
        constants.browser_lib.wait_until_page_contains_element(locator = '//*[@id="investments-table-object_length"]//label//select', timeout = 30000)
        constants.browser_lib.select_from_list_by_index('//*[@id="investments-table-object_length"]//label//select', '3')
        constants.browser_lib.wait_until_page_does_not_contain_element('//*[@id="investments-table-object_paginate"]//span//a[2]', timeout = 30000)
        
        print('The investment table has been setuped sucessfully!')
    except:
        raise Exception('The individual investment table, failed to load, try again later!')


# Function that extract individual investment table and get all UII links 
def scrapping_individual_investments_table(term):
    row = 3
    dt = constants.tables_lib.create_table({'UII':[],'Bureau':[],'Investment Title':[],'Total FY2021 Spending ($M)':[],'Type':[],\
                                            'CIO Rating':[],'of Projects':[]})
    links = []
    nLinks = 0

    while True:
        try:
            # Get row cells
            uii = constants.browser_lib.get_table_cell('//*[@id="investments-table-object"]', row, 1)
            bureau = constants.browser_lib.get_table_cell('//*[@id="investments-table-object"]', row, 2)
            title = constants.browser_lib.get_table_cell('//*[@id="investments-table-object"]', row, 3)
            total = constants.browser_lib.get_table_cell('//*[@id="investments-table-object"]', row, 4)
            type_ = constants.browser_lib.get_table_cell('//*[@id="investments-table-object"]', row, 5)
            cioRating = constants.browser_lib.get_table_cell('//*[@id="investments-table-object"]', row, 6)
            ofProjects = constants.browser_lib.get_table_cell('//*[@id="investments-table-object"]', row, 7)
            
            row = row + 1
            
            # Add the row to dataframe
            constants.tables_lib.add_table_row(dt, [uii, bureau, title, total, type_, cioRating, ofProjects])
            try:
                # Verify if the UII has a link and add to links list
                selectorUIILink = '//*[@id="investments-table-object"]//tbody//tr[{0}]//td[1]//a'
                selectorUIILink = selectorUIILink.format(row - 3)
                link = constants.browser_lib.get_element_attribute(selectorUIILink, 'href')
                links.append(link)
                nLinks = nLinks + 1
            except:
                continue
        except:
            break

    print('The Investment table was successfully extracted!')
    print('{0} links has been identified.'.format(nLinks))
    return dt, links, nLinks


