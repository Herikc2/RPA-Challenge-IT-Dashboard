# Packages
from RPA.Browser.Selenium import Selenium
from RPA.PDF import PDF
from modulos import constants, agencie, individual_investment, pdfs_management


# Function to open browser
def open_the_website(url):
    constants.browser_lib.open_available_browser(url)
    constants.browser_lib.maximize_browser_window()

    print('Website has been opened: {0}'.format(url))


def main():
    try:
        term = constants.AGENCY

        # Opening website and click 'DIVE IN' 
        open_the_website("https://itdashboard.gov/")
        constants.browser_lib.click_element_when_visible('xpath://*[@id="node-23"]//div//div//div//div//div//div//div//a')

        # Get all values about agencies and save to excel
        agencies = agencie.get_values()
        constants.tables_lib.write_table_to_csv(agencies, constants.OUTPUT_PATH + '\Agencies.csv', True)
        print('Agencies and spend amount has been extracted and saved to excel.')

        # Get row and column where is located agencie
        row, column = agencie.map_agencie(agencies, term)
        print('Agency has been located: {0}'.format(term))
        agencie.select_agencie(row, column)
        print('Agency has been selected.')

        # Getting Individual Investment Table and their links
        individual_investment.setup_individual_investment_table()
        individualInvestment, linksIndividualInvestment, nLinks = individual_investment.scrapping_individual_investments_table(term)

        # Save investment table to excel
        path = constants.OUTPUT_PATH + '\{0}.csv'.format(term)
        constants.tables_lib.write_table_to_csv(individualInvestment, path, True)
        print('The Investment table was saved.')

        # Downloading and moving all PDFs to output folder
        pathPDFs = pdfs_management.download_pdfs(linksIndividualInvestment, nLinks)

        # Comparing PDF infos
        dtCompareInfos = pdfs_management.compareInfos(individualInvestment, pathPDFs, nLinks)

        path = constants.OUTPUT_PATH + '\{0}_Compare_Infos.csv'.format(term)
        constants.tables_lib.write_table_to_csv(dtCompareInfos, path, True)

        print('\nAll PDFs has been compared with the investment table!')

    finally:
        print("Finally")
        constants.browser_lib.close_all_browsers()


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()
