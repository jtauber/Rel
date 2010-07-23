from dep import DependencyAnalysis

from rel import Rel

r = Rel(("x", "y"))
r.add(x="A", y=1)
r.add(x="B", y=1)
r.add(x="C", y=1)
r.add(x="A", y=2)
r.add(x="C", y=2)

d = DependencyAnalysis(r)

# this will print "('B',) : (1,)" because the only dependency between the x
# and y columns is that if x = "B" then y can only be 1.

for t in d.find_dependencies(("x",), ("y",)):
    print str(t[0]), ":", ", ".join([str(v) for v in t[1]])

r.add(x="B", y=2)

d2 = DependencyAnalysis(r)

# this will print nothing because there is now no dependency between x and y
# in other words, y can take all values regardless of what x is.

for t in d2.find_dependencies(("x",), ("y",)):
    print str(t[0]), ":", ", ".join([str(v) for v in t[1]])
