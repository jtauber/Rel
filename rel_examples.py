from rel import Rel, PROJECT, RESTRICT, INTERSECT, UNION, PROJECT_VIEW, RESTRICT_VIEW

dept = Rel(("DNO", "DNAME", "BUDGET"))

dept.add(DNO="D1", DNAME="Marketing", BUDGET="10M")
dept.add(DNO="D2", DNAME="Development", BUDGET="12M")
dept.add(DNO="D3", DNAME="Research", BUDGET="5M")

emp = Rel(("ENO", "ENAME", "DNO", "SALARY"))

emp.add(ENO="E1", ENAME="Lopez", DNO="D1", SALARY="40K")
emp.add(ENO="E2", ENAME="Cheng", DNO="D1", SALARY="42K")
emp.add(ENO="E3", ENAME="Finzi", DNO="D2", SALARY="30K")

emp2 = Rel(("ENO", "ENAME", "DNO", "SALARY"))
emp2.add_multiple([
    dict(ENO="E3", ENAME="Finzi", DNO="D2", SALARY="30K"),
    dict(ENO="E4", ENAME="Saito", DNO="D2", SALARY="35K")
])

dept.display()
emp.display()
emp2.display()

print
print "PROJECT"
PROJECT(emp, ("ENO", "ENAME")).display()

print
print "RESTRICT"
RESTRICT(emp, lambda tup: tup["SALARY"] <= "40K").display()

print
print "INTERSECT"
INTERSECT(emp, emp2).display()

print
print "UNION"
UNION(emp, emp2).display()

p = PROJECT_VIEW(emp, ("ENO", "ENAME"))
p.display()
emp.add(ENO="E4", ENAME="Saito", DNO="D2", SALARY="35K")
p.display()

r = RESTRICT_VIEW(emp2, lambda tup: tup["SALARY"] <= "40K")
r.display()
emp2.add(ENO="E1", ENAME="Lopez", DNO="D1", SALARY="40K")
r.display()
