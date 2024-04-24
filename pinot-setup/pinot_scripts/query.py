from pinotdb import connect

conn = connect(host='localhost', port=8099, path='/query', scheme='http')
curs = conn.cursor()
curs.execute("""
    SELECT SUM(score) from transcript where firstName='Natalie'
""")
for row in curs:
    print(row)