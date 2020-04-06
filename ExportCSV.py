import csv

def ExportCSVFileData(path, fileName, firstQuestion, results):    
    csvFileName = path + fileName + ".csv"
    with open(csvFileName, mode='w', newline='') as exportFile:
        exportWriter = csv.writer(exportFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        exportWriter.writerow(['Name', fileName])
        exportWriter.writerow(['Please provide an overall score between 0-100"%" of how engaged you think the child was:', firstQuestion])
        exportWriter.writerow(['Time in Video', 'Slider Value'])
        for time in results:
            exportWriter.writerow([time, results[time]])

def ExportCSVUserData(path, userName, organisation, block, secondQuestion, thirdQuestion, fourthQuestion):    
    csvFileName = path + ".csv"
    with open(csvFileName, mode='w', newline='') as exportFile:
        exportWriter = csv.writer(exportFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        exportWriter.writerow(['Name', userName])
        exportWriter.writerow(['Organistion', organisation])
        exportWriter.writerow(['Block', block])
        exportWriter.writerow(['What does engagement look like/mean to you?', secondQuestion])
        exportWriter.writerow(['What particular signs did you use to determine engagement?', thirdQuestion])
        exportWriter.writerow(['If you have any additional feedback, notes or comments you would like to add, please write them here?', fourthQuestion])