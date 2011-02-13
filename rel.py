class Rel:
    
    def __init__(self, record_class):
        self._record_class = record_class
        self._records = set()
    
    def add(self, record=None, **kwargs):
        if record is None:
            record = self._record_class(**kwargs)
        
        self._records.add(record)
    
    def display(self):
            """
            display the relation in tabular form.
            """
            
            # if it seems inefficient that display uses self.tuples() rather than
            # self.tuples_, it is because that way it will work on views where
            # tuples() is dynamic
            
            columns = range(len(self._record_class._fields))
            
            col_width = [len(self._record_class._fields[col]) for col in columns]
            
            for record in self._records:
                for col in columns:
                    col_width[col] = max(col_width[col], len(record._asdict()[self._record_class._fields[col]]))
            
            hline = ""
            for col in columns:
                hline += "+-" + ("-" * col_width[col]) + "-"
            hline += "+"
            
            def line(row):
                l = ""
                for col in columns:
                    value = row[col]
                    l += "| " + value + (" " * (col_width[col] - len(value))) + " "
                l += "|"
                return l
            
            print hline
            print line(self._record_class._fields)
            print hline
            
            for record in self._records:
                print line([record._asdict()[self._record_class._fields[col]] for col in columns])
            
            print hline


def RESTRICT(orig_rel, restriction):
    new_rel = Rel(orig_rel._record_class)
    for record in orig_rel._records:
        if restriction(record):
            new_rel.add(record)
    return new_rel


def INTERSECT(rel_1, rel_2):
    assert rel_1._record_class == rel_2._record_class
    new_rel = Rel(rel_1._record_class)
    for record in rel_1._records.intersection(rel_2._records):
        new_rel.add(record)
    return new_rel


def UNION(rel_1, rel_2):
    assert rel_1._record_class == rel_2._record_class
    new_rel = Rel(rel_1._record_class)
    for record in rel_1._records.union(rel_2._records):
        new_rel.add(record)
    return new_rel
