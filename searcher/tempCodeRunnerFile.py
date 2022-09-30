c.execute("""CREATE TABLE university1 (
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
#     c.execute(f"insert into university values {row}")
# conn.commit()