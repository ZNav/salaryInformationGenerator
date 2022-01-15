import csv
import scrapy
from datetime import datetime

print('Generating .csv file...')
jobs = open("jobs.txt", "r").read().split("\n")
cities = open("cities.txt", "r").read().split("\n")

#class
class salary(scrapy.Spider):
    name = 'salary'

    header = ['salary', 'reportsDone','jobTitle','location','payType','dateTime']
    with open('salaryInformation.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        file.close()

    def start_requests(self):
        global links
        global ig
        for i in cities:
            for x in jobs:
                ig = i
                yield scrapy.Request(url = 'https://www.indeed.com/career/'+str(x)+'/salaries/'+str(i), callback=self.parse)
            


    def parse(self, response):
        global ig
        salary = (response.xpath('//div[@data-testid="avg-salary-value"]/text()').extract())
        if(',' in salary[0]):
            payType = 'salary'
        else:
            payType = 'hourly'
        salary[0] = salary[0].replace('$','')
        salary[0] = salary[0].replace(',','')
        print('salary: '+str(salary[0]))
        salary = (str(salary[0]))
        reports = (response.xpath('//span[@data-testid="sal-agg-nonbase__salary-reported"]/text()').extract())
        reportsDone = reports[0].split(' ')
        reportsDone[0] = reportsDone[0].replace('k','00')
        reportsDone[0] = reportsDone[0].replace('.','')
        print('reports done: '+str(reportsDone[0]))
        reportsDone = (str(reportsDone[0]))
        urlList = response.request.url.split('/')
        jobTitle = urlList[-3]
        location = urlList[-1]
        print('job title: '+str(jobTitle))
        print('location: '+str(location))
        info = [float(salary), int(reportsDone), jobTitle, location, payType,datetime.now()]
        with open('salaryInformation.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(info)
            file.close()

    print('Generated file: salaryInformation.csv')