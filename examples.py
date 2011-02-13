#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from urecord import Record
from rel import Rel


class Department(Record("DNO", "DNAME", "BUDGET")):
    pass


class Employee(Record("ENO", "ENAME", "DNO", "SALARY")):
    pass


dept = Rel(Department)

# can add with keyword args
dept.add(DNO="D1", DNAME="Marketing", BUDGET="10M")
dept.add(DNO="D2", DNAME="Development", BUDGET="12M")

# or with a Record object
research = Department(DNO="D3", DNAME="Research", BUDGET="5M")
dept.add(research)


emp = Rel(Employee)

emp.add(ENO="E1", ENAME="Lopez", DNO="D1", SALARY="40K")
emp.add(ENO="E2", ENAME="Cheng", DNO="D1", SALARY="42K")

finzi = Employee(ENO="E3", ENAME="Finzi", DNO="D2", SALARY="30K")
emp.add(finzi)

emp2 = Rel(Employee)

emp2.add(ENO="E3", ENAME="Finzi", DNO="D2", SALARY="30K")
emp2.add(ENO="E4", ENAME="Saito", DNO="D2", SALARY="35K")


dept.display()
print
emp.display()
print
emp2.display()


# @@@ not sure what PROJECT would mean with µrecord


print
print "RESTRICT"
emp.restrict(lambda record: record.SALARY <= "40K").display()


print
print "INTERSECT"
emp.intersection(emp2).display()


print
print "UNION"
emp.union(emp2).display()
