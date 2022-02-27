# Packages
from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
from modulos import constants


# Function to read PDF and extract "Name of This Investment" and Unique Investment Identifier"
def read_pdf(pathPDF):
    text = constants.pdf_lib.get_text_from_pdf(source_path = pathPDF, pages = 1, trim = False)
    
    nameOfThisInvestmentPDF = text[1].split("Name of this Investment: ")[1].split("2. Unique Investment Identifier (UII):")[0]
    uniqueInvestmentIdentifierPDF = text[1].split("2. Unique Investment Identifier (UII): ")[1].split("Section B:")[0]

    return nameOfThisInvestmentPDF, uniqueInvestmentIdentifierPDF


# Function to compare PDF info with Investment Table and return a dataframe
def compareInfos(dt, pathPDFs, nLinks):
    dtCompare = constants.tables_lib.create_table({'Name of This Investment PDF':[],'Unique Investment Identifier PDF':[], 'Investment Title Table':[],\
                                        'UII Table':[],'Comparison':[]})
    count = 0
    i = 0
    
    while True:
        try:
            for pathPDF in pathPDFs:            
                pdfName = pathPDF.split('\\')[-1].replace('.pdf', '')

                if pdfName == dt[i][0]:
                    nameOfThisInvestmentPDF, uniqueInvestmentIdentifierPDF = read_pdf(pathPDF)

                    if (nameOfThisInvestmentPDF in dt[i][2] or dt[i][2] in nameOfThisInvestmentPDF) and\
                        (uniqueInvestmentIdentifierPDF in dt[i][0] or dt[i][0] in uniqueInvestmentIdentifierPDF):
                        comparison = 'True'
                    else:
                        comparison = 'False'
                        
                    constants.tables_lib.add_table_row(dtCompare, [nameOfThisInvestmentPDF, uniqueInvestmentIdentifierPDF, dt[i][2], dt[i][0], comparison])
                    count = count + 1
                    break
                    
            i = i + 1
        except:
            break
                
        if count >= nLinks:
            break
    
    return dtCompare            


# Function that get a specific PDF and move to output folder
def get_pdf(link, fileName):
    # Go to link and download PDF
    constants.browser_lib.go_to(link)
    constants.browser_lib.click_element_when_visible('//*[@id="business-case-pdf"]//a')

    path = constants.OUTPUT_PATH + '\\' + str(fileName)

    return path


# Function that loop to all UII links
def download_pdfs(links, nLinks):
    strTemplate = '/{0} PDF downloaded'.format(nLinks)
    pathPDFs = []
    i = 0

    for link in links:
        fileName = str(link.split('/')[-1]) + '.pdf'
        pathPDF = get_pdf(link, fileName)

        i = i + 1
        pathPDFs.append(pathPDF)
        print(str(i) + strTemplate)

    print('{0} PDFs was successfully downloaded!'.format(i))

    return pathPDFs


