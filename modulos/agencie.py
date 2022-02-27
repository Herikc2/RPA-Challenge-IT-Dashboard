# Packages
from RPA.Browser.Selenium import Selenium
from RPA.Tables import Tables
from modulos import constants


# Function that go to the agencie choosed by user
def select_agencie(row, column):
    selectorViewAgencie = '//*[@id="agency-tiles-widget"]//div//div[{0}]//div[{1}]//div/div/div/div[2]//a'
    selectorViewAgencie = selectorViewAgencie.format(row, column)

    constants.browser_lib.click_element(selectorViewAgencie)


# Function that get all values about agencies and return a dataframe
def get_values():
    column = 1
    row = 1
    rowError = False
    columnError = False
    
    dt = constants.tables_lib.create_table({'Agencie':[],'Spend amount':[]})
    
    constants.browser_lib.wait_until_page_contains_element('//*[@id="agency-tiles-widget"]//div//div[1]//div[1]//div//div//div//div[1]//a//span[1]')
    
    while True:       
        try:
            # Get name from agencie
            selectorGetName = '//*[@id="agency-tiles-widget"]//div//div[{0}]//div[{1}]//div//div//div//div[1]//a//span[1]'
            selectorGetName = selectorGetName.format(row,column)
            agencie = constants.browser_lib.get_text(selectorGetName)
            
            # Get spend amout from agencie
            selectorGetValue = '//*[@id="agency-tiles-widget"]//div//div[{0}]//div[{1}]//div//div//div//div[1]//a//span[2]'
            selectorGetValue = selectorGetValue.format(row,column)
            spendAmount = constants.browser_lib.get_text(selectorGetValue)

            # Add row to dataframe
            column = column + 1
            columnError = False
            
            constants.tables_lib.add_table_row(dt, [agencie, spendAmount])
        except:
            # Verify is has finished all agencies
            if columnError:
                rowError = True
                break

            columnError = True

            row = row + 1
            column = 1

        if rowError and columnError:
            break

    return dt


# Function to mapping where is the agencie choosed by user
def map_agencie(dt, term):
    i = 0
    
    while True:
        try:
            if dt[i][0] == term:
                break
            i = i + 1
        except:
            break
            
    index = i + 1
    row = (index // 3) + 1
    if index <= 3:
        row = 1

    column = (index % 3)
    if column == 0:
        column = 3

        if index > 3:
            row = row - 1

    return row, column


