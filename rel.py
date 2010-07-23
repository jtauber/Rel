
# Relational Python
# by James Tauber
#
# Improvements to Rel class suggested by Kent Johnson


class Rel:
    """
    A relation.
    
    Essentially a set of dictionaries (called tuples) where each dictionary has 
    identical keys (called attributes).
    
    Internally, each tuple is stored as a Python tuple rather than a dictionary
    and the relation also keeps an ordered list of the attributes which is used
    as the index into the tuples.
    """
    
    def __init__(self, attributes, dictset=set()):
        """
        create a relation with the given attributes.
        """
        
        self.attributes_ = tuple(attributes)
        self.tuples_ = set()
        self.tuples_.update(set([self._convert_dict(d) for d in dictset]))
    
    def attributes(self):
        """
        return the set of attributes.
        """
        
        return set(self.attributes_)
    
    def _convert_dict(self, tup):
        """
        convert a dictionary to the internal representation of a tuple.
        """
        
        # don't convert if already a tuple
        if isinstance(tup, tuple):
            return tup
        else:
            return tuple([tup[attribute] for attribute in self.attributes_])
    
    def add(self, tup=None, **kwargs):
        """
        add the given dictionary or keyword args to the relation as a tuple.
        """
        
        if tup is None:
            tup = kwargs
        self.tuples_.add(self._convert_dict(tup))
    
    def add_tuple(self, tup):
        """
        add the given python tuple to the relation
        """
        self.tuples_.add(tup)
    
    def add_multiple(self, tupset):
        """
        add the given dictionaries to the relation as tuples.
        """
        
        self.tuples_.update(set([self._convert_dict(tup) for tup in tupset]))
    
    def _tuples(self):
        return self.tuples_
    
    def tuples(self):
        """
        return a generator over the tuples in this relation.
        
        Each item the generator yields is a dictionary.
        """
        
        for tup in self._tuples():
            yield dict(zip(self.attributes_, tup))
    
    def display(self):
        """
        display the relation in tabular form.
        """
        
        # if it seems inefficient that display uses self.tuples() rather than
        # self.tuples_, it is because that way it will work on views where
        # tuples() is dynamic
        
        columns = range(len(self.attributes_))
        
        col_width = [len(self.attributes_[col]) for col in columns]
        
        for tupdict in self.tuples():
            tup = self._convert_dict(tupdict)
            for col in columns:
                col_width[col] = max(col_width[col], len(tup[col]))
        
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
        print line(self.attributes_)
        print hline
        
        for tup in self.tuples():
            print line(self._convert_dict(tup))
        
        print hline


def project(orig_dict, attributes):
    return dict([item for item in orig_dict.items() if item[0] in attributes])


def PROJECT(orig_rel, attributes):
    return Rel(attributes, [project(tup, attributes) for tup in orig_rel.tuples()])


def RESTRICT(orig_rel, restriction):
    return Rel(orig_rel.attributes(), [tup for tup in orig_rel.tuples() if restriction(tup)])


def INTERSECT(rel_1, rel_2):
    assert rel_1.attributes() == rel_2.attributes()
    return Rel(rel_1.attributes(), rel_1._tuples().intersection(rel_2._tuples()))


def UNION(rel_1, rel_2):
    assert rel_1.attributes() == rel_2.attributes()
    return Rel(rel_1.attributes(), rel_1._tuples().union(rel_2._tuples()))


class PROJECT_VIEW(Rel):
    
    def __init__(self, orig_rel, attributes):
        Rel.__init__(self, attributes)
        self.orig_rel = orig_rel
    
    def add(self, tup):
        raise Exception # pragma: no cover
    
    def tuples(self):
        for tup in self.orig_rel.tuples():
            yield project(tup, self.attributes_)


class RESTRICT_VIEW(Rel):
    
    def __init__(self, orig_rel, restriction):
        Rel.__init__(self, orig_rel.attributes())
        self.orig_rel = orig_rel
        self.restriction = restriction
    
    def add(self, tup):
        raise Exception # pragma: no cover
    
    def tuples(self):
        for tup in self.orig_rel.tuples():
            if self.restriction(tup):
                yield tup
