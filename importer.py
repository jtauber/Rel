from rel import Rel

def load_file(filename, attributes):
    """
    load the space-delimited file with the given filenames assuming the
    attributes given (as a pythontuple)
    """
    
    r = Rel(attributes)
    
    for line in open("ccat.txt"):
        r.add_tuple(tuple(line.strip().split()))
    
    return r
