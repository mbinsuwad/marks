from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import sqlite3

# from try import chunk_students
# Create your views here.

DB = '2022.sqlite3'
table_name = "scraped"


conn = sqlite3.connect(DB, check_same_thread=False)
c = conn.cursor()

def countRegistorsOnCollegeAndSpecialty(table, college, specialty):
    c.execute(f"SELECT specialty FROM {table} WHERE specialty = '{specialty}' AND college = '{college}'")
    return len(c.fetchall())

def countAcceptedsNum (table_name):
    return len(set(c.execute(f"SELECT id, name FROM {table_name} where accepted").fetchall()))

def countRegistersNum (table_name):
    return len(set(c.execute(f"SELECT id, name FROM {table_name}").fetchall()))
# def numberOfAccepteds():
    # return len(c.execute("SELECT id FROM scraped WHERE college = '{college}' AND specialty = '{specialty}' AND "))

def countTestedOnCollegeAndSpecialty(college, specialty):
        return len(c.execute(f"SELECT id FROM {table_name} WHERE college = '{college}' AND specialty = '{specialty}' AND test_mark >= 2 ").fetchall())

def countAllRegestorsOnCollegeAndSpecialty(college, specialty):
        return len(c.execute(f"SELECT id FROM {table_name} WHERE college = '{college}' AND specialty = '{specialty}'").fetchall())
        

def countAcceptedOnCollegeAndSpecialty(college, specialty):
        return len(c.execute(f"SELECT id FROM {table_name} WHERE college = '{college}' AND specialty = '{specialty}' AND accepted").fetchall())


def get_ids(entry_name):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    ids = list()
    c.execute(f"SELECT id, name FROM {table_name}")
    contant = c.fetchall()
    for id, name in contant:
        if set(entry_name.split()).issubset(name.split()) and id not in ids:
            ids.append(id)
    return ids

def get_student(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(f"SELECT seq, id, name, male, scondary_shool, test, finall, specialty, college, accepted, accepted_seq FROM {table_name} WHERE id = {id}")
    data = c.fetchall()
    student = Student()
    student.full_name = data[0][2]
    student.male = data[0][3]
    student.goals = []
    # student.secondary_school_mark = data[0][1]
    for special in data:
        goal = Wish()
        goal.special = special[7]
        goal.college = special[8]
        goal.accepted = special[9]
        goal.accepted_seq = special[10]
        goal.seq = special[0]
        goal.marks = special[4:7]
        if goal.accepted:
            student.goals.insert(0,goal)
        else:
            student.goals.append(goal)
        goal.accepted_count = len(c.execute(f"SELECT id FROM {table_name} WHERE college = '{goal.college}' AND specialty = '{goal.special}' AND accepted").fetchall())
        goal.count_all = countAllRegestorsOnCollegeAndSpecialty(goal.college, goal.special)
    return student


class Wish():
    special = ''
    college = ''
    count_all = countRegistorsOnCollegeAndSpecialty("scraped", college, special)
    marks = []
    accepted = False
    # if accepted:
    accepted_seq = 0
    accepted_count = -75
    seq = 0
    
class Student():
    full_name = ''
    male = True
    id = ''
    # secondary_school_mark = 0
    goals = []
s = {
    'full_name': '',
    'male': True,
    'id': '',
    'goals': []
}
w = {
    'special' : '',
    'college' : '',
    'count_all' : 0,
    'marks' : [],
    'accepted' : False,
    # if accepted:
    'accepted_seq' : 0,
    'accepted_count' : -75,
    'seq' : 0,

}


def chunks(list):
    lst = []
    try:
        while True:
            lst.append(list[:5])
            for u in range(5):del list[0]
    except: pass
    return lst

visit_counter = 0    
search_counter = 0

def postCounter():
    global search_counter
    search_counter += 1

def visitCounter ():
    global visit_counter
    visit_counter +=1


class College:
    name = ''
    specialties = []

class College():
    name = list[0]
    specialties = []

    def __init__(self,list) -> None:
        self.name = list[0]
        self.specialties = list[1]
    
    def __str__(self):
        return f"{self.name} : {self.specialties}"

def get_specialty(college):
    c.execute(f"select specialty, register, tested, accepted from university1 where college = '{college}'")
    all = c.fetchall()
    return all

def get_colleges():
    colleges = []
    for coll in c.execute(f"select college from university1").fetchall():
        if coll[0] not in colleges:colleges.append(coll[0])
    return colleges

def university():
    list = []
    colleges = get_colleges()
    for c1 in range(len(colleges)):
        college = [colleges[c1], get_specialty(colleges[c1])]
        entry = College(college)
        list.append(entry)
    return list

def names(request):
    entry = request.GET['entry']
    all = []
    for name in c.execute(f"select name from {table_name}").fetchall():
        if name[0] not in all and name[0].startswith(entry):
            all.append(name[0])
    if len(all)>20:
        names = all[:20]
    else:names = all
        
    return JsonResponse({
        "names": names
    })



######## THE MAIN FUNCTION #########
def index (request):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    entry_name = ''
    if request.method == "POST" and request.POST.get('q', entry_name) != '':
        entry_name = request.POST.get('q', entry_name)
        page = int(request.POST.get("page"))
        postCounter()
        students = []
        chunksList = list(chunks(get_ids(entry_name)))
        print(chunksList)
        for id in chunksList[int(page)-1]:
            students.append(get_student(id))
        c.close()
        # if len(students) == 0:
        #     return render(request, "index.html",{
        #     "students" : [],
        #     "visitors": visit_counter,
        #     "posting_times": search_counter,
        #     "university" : university(),
        #     "registers" : countRegistersNum("scraped"),
        #     "accepteds" : countAcceptedsNum("scraped"),
            
        # })

        pages = len(chunksList)
        return render(request, "index.html",{
            # "page" : page,
            "visitors": visit_counter,
            "posting_times": search_counter,
            "entry_name" : entry_name,
            "pages" : range(1,pages+1),
            "students" : students,
            "visitors": visit_counter,
            "posting_times": search_counter,
        })   

    visitCounter()
    return render(request, "index.html",{
        "students" : [],
        "visitors": visit_counter,
        "posting_times": search_counter,
        "university" : university(),
        "registers" : countRegistersNum("scraped"),
        "accepteds" : countAcceptedsNum("scraped"),
        
    })
