import sqlite3

conn = sqlite3.connect('2022.sqlite3')
c = conn.cursor()

def getColleges():
    lst= []
    for college in c.execute("select college, specialty from scraped").fetchall():
        if college not in lst:
            lst.append(college)
    return lst
def getSpecialties(college):
    lst = []
    for special in c.execute(f"select specialty from scraped where college = '{college}'").fetchall():
        if special[0] not in lst:
            lst.append(special[0])
    return lst

# c.execute("""CREATE TABLE university1 (
#     college text,
#     specialty text,
#     register integer,
#     tested integer,
#     accepted integer
# )""")
# conn.commit()


# for co in getColleges():
#     college = co[0]
#     specialty = co[1]
#     register = len(c.execute(f"select id from scraped where college = '{college}' and specialty = '{specialty}'").fetchall())
#     tested = len(c.execute(f"select id from scraped where college = '{college}' and specialty = '{specialty}' and test<2").fetchall())
#     accepted = len(c.execute(f"select id from scraped where college = '{college}' and specialty = '{specialty}' and accepted").fetchall())
#     row=(college, specialty, register, tested, accepted)
#     c.execute(f"insert into university1 values {row}")
# conn.commit()
# print(c.execute("select * from university1").fetchall())
# print("Done")