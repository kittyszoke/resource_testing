import os
from sys import modules
from pysondb import db
import datetime
import json
import time

def removeHeader(file):
    with open(file, "r") as f:
        lines = f.readlines()
    with open(file, "w") as f:
        lineNum = 1
        for line in lines:
            if lineNum != 245:
                f.write(line)
            lineNum += 1

# If you want to append test records or just update them
append = False

# ct stores current time
ct = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
print("Timestamp:", ct)

pwd = os.path.abspath(os.getcwd())

database = db.getDb(f"{pwd}/backend/database/db.json")
testReportDb = db.getDb(f"{pwd}/backend/database/test_section_terraform_results.json")
trainees = database.getAll()

os.system(f'mkdir -p test-repo-terraform')

for trainee in trainees:
    id = trainee['id']
    name = trainee['first_name'].lower().strip()+'-'+trainee['last_name'].lower().strip()
    biturl = trainee['bitbucket_url']   
    # pulls users repository
    if biturl != '' :
        
        os.system(f'git submodule add --force {biturl} test-repo-terraform/{name}')
        
        
        # Create list for test records
        testRecords = []
        directories = os.listdir(f'test-repo-terraform/{name}/terraform/pytest')

        directories_filtered = []

        for directory in directories:
            # If the first character is =0 then append
            directory[0]
            if directory[0] == '0':
                directories_filtered.append(directory)
        print(directories_filtered)

        for directory in directories_filtered:
            print(directory)
            time.sleep(3)

            # Generates test result json files
            os.system(f'pytest --json-report -v --json-report-file=terraform_report.json {pwd}/test-repo-terraform/{name}/terraform/pytest/{directory}')
            
            # Reads json and saves results
            with open(f'{pwd}/terraform_report.json') as json_file:
                data = json.load(json_file)
            
            # Notes if exercise has been passed (all tests for exercise has been passed)
            complete = ('passed' in data['summary']) and (data['summary']['passed'] == data['summary']['total'])
            complete = (data['summary']['total'] == 0) or complete
            testRecords.append({
                    'directory' : directory,
                    'complete' : complete,
                    'results' : data})
            
            # Generates test result html file
            os.system(f'pytest --html=backend/templates/html_reports/test_section_terraform_html/{id}-{directory}-terraform.html {pwd}/test-repo-terraform/{name}/terraform/pytest/{directory}')
            
            # Generates test result html file
            #os.system(f'pytest --pylint --html=backend/templates/html_reports/{id}-{directory}-docker.html {pwd}/test-repo-docker/{name}/docker/pytest/apache_test/{directory}')
            

            # Removes heading from html report
            html_file_path = f'{pwd}/backend/templates/html_reports/test_section_terraform_html/{id}-{directory}-terraform.html'
            removeHeader(html_file_path)

        # Adds the test results to the database 
        current_test_results = testReportDb.getByQuery({
            "trainee_id": id})
        # If appending data or this is the first results collected for trainee
        if (append or (len(current_test_results)==0)):
            testReportDb.add({
                'trainee_id' : trainee['id'],
                'start_time' : ct,
                'test_records' : testRecords  
            })
        # Otherwise update last record
        else:
            last_result = current_test_results.pop()
            test_results_id = last_result['id']
            testReportDb.updateById(test_results_id, {
                'trainee_id' : trainee['id'],
                'start_time' : ct,
                'test_records' : testRecords  
            })

    #Deletes trainee's repo
    if os.path.isdir(f'test-repo-terraform/{name}'):
        os.system(f'git rm -rf test-repo-terraform/{name}')
        
    # Deletes trainee's report file
    if os.path.isfile('terraform_report.json'):
        os.system('rm terraform_report.json')

# Delete from git modules 
if os.path.isdir('test-repo-terraform'):
    os.system('rm -rf .git/modules/test-repo-terraform')
    os.system('rm -rf test-repo-terraform')