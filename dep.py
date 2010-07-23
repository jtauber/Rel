from collections import defaultdict

def cartesian_product(sets, done=()):
    if sets:
        for element in sets[0]:
            for tup in cartesian_product(sets[1:], done + (element,)):
                yield tup
    else:
        yield done

def non_contig_slice(seq, indices):
    result = ()
    for i in indices:
        result += (seq[i],)
    return result

class DependencyAnalysis:
    
    def __init__(self, rel):
        self.rel = rel
        self.possible_values = defaultdict(set)
        
        for tup in self.rel.tuples():
            for attribute, value in tup.items():
                self.possible_values[attribute].add(value)
    
    def find_dependencies(self, cols_i, cols_j):
        for i_value in cartesian_product(non_contig_slice(self.possible_values, cols_i)):
            j_values = set()
            for tup in self.rel.tuples():
                if non_contig_slice(tup, cols_i) == i_value:
                    j_values.add(non_contig_slice(tup, cols_j))
            if j_values < set(cartesian_product(non_contig_slice(self.possible_values, cols_j))):
                yield i_value, j_values
