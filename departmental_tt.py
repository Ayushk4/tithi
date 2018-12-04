import requests
import json
from bs4 import BeautifulSoup

COOKIE = '933C57C89AF16DFDB7B7125F5DD20767.worker3'

file = open('depts.txt','r')
DEPT_CODES = file.read().split('\n')
EXAMINATIONS = ['END','MID']
SEMESTERS = ['AUTUMN','SPRING']
ACAD_YEAR = 8 # For 2018-19
cookies = {'JSESSIONID' : COOKIE} #'JSID#/Acad' : COOKIE}
headers = {
        'timeout': '20',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
        'Referer': 'https://erp.iitkgp.ac.in/Acad/exam/view_dept_exam_tt.jsp?action=first'
        }

r = requests.get('https://erp.iitkgp.ac.in/Acad/exam/view_dept_exam_tt.jsp?action=first')

def parseandsave(html_page,exam_data,year,semester,exam):
    soup = BeautifulSoup(html_page, 'html.parser')
    subject_rows = soup.findAll("tr", {"bgcolor": "white"})

    print(year,semester,exam)

    for subject_row in subject_rows:
        subject_tags = subject_row.findAll("td")

        course_code = subject_tags[1].text
        course_name = subject_tags[2].text
        start = subject_tags[4].text
        end = subject_tags[5].text
        room = subject_tags[6].text
        student_count = subject_tags[7].text

        current_course_exam_data = {}
        current_course_exam_data['start'] = start
        current_course_exam_data['end'] = end
        current_course_exam_data['room'] = room
        current_course_exam_data['student_count'] = student_count

        print( current_course_exam_data)

        if course_code not in exam_data:
            exam_data[course_code] = {}
            exam_data[course_code]["course_name"] = course_name
            exam_data[course_code]["exam_data"] = {}
        print(exam_data)
        if year not in exam_data[course_code]["exam_data"]:
            exam_data[course_code]["exam_data"][year] = {}
        
        if semester not in exam_data[course_code]["exam_data"][year]:
            exam_data[course_code]["exam_data"][year][semester] = {}
        
        exam_data[course_code]["exam_data"][year][semester][exam] = current_course_exam_data

        print("\n\n")
        print(exam_data)

        import time
        time.sleep(3)
        print("\n\n\n\n\n")

    print(subjects_data)

def department_time_table():

    exam_data = {}
    with open('data_departmental.json') as f:
        exam_data = json.load(f)
    
    print(exam_data)
#    exam_data = {"CL60001" : "DSFSD"}
    for i in range (3,ACAD_YEAR + 1):
        year = '201{}-201{}'.format(i,i+1)
        print('\n-----------------------------------------------------')
        print('\nCollecting data for academic_year ' + year)
        print('\n-----------------------------------------------------')
        for semester in SEMESTERS:
            print('\n\t------------')
            print('\n\tCollecting data for ' + semester + ' semester')
            print('\n\t------------')
            for exam in EXAMINATIONS:
                print('\n\t\t--------')
                print('\n\t\tCollecting data for ' + exam + '-sems')
                print('\n\t\t---------')
                for dept in DEPT_CODES:
                    print('\n\t\t\tCollecting data for ' + dept)
                    payload = {
                                'session' : '201{}-201{}'.format(i,i+1),
                                'semester' : semester,
                                'exam_type' : exam,
                                'dept' : dept
                                }

                    r = requests.post('https://erp.iitkgp.ac.in/Acad/exam/view_dept_exam_tt.jsp?action=second',cookies = cookies,data = payload, headers = headers)
                    
                    if 'No data available' not in r.text:    
                        print(r)
                        print(r.text)
                        parseandsave(r.text,exam_data,str(year),semester,exam)
                        print('----------------------------')
                        import time
                        time.sleep(10000)

if __name__ == '__main__':
    department_time_table()
