from functools import wraps


def union_compatible(method):
    """Declare a set operation as requiring union-compatibility."""

    @wraps(method)
    def wrapper(self, other_rel):
        assert self._record_class._fields == other_rel._record_class._fields
        result = method(self, other_rel)
        result._record_class = self._record_class
        return result
    return wrapper


class Rel(set):

    def __init__(self, record_class):
        self._record_class = record_class
        super(Rel, self).__init__()

    def add(self, record=None, **kwargs):
        if record is None:
            record = self._record_class(**kwargs)
        super(Rel, self).add(record)

    def restrict(self, restriction):
        new_rel = type(self)(self._record_class)
        for record in self:
            if restriction(record):
                new_rel.add(record)
        return new_rel

    intersection = union_compatible(set.intersection)
    union = union_compatible(set.union)

    def rename(self, **mapping):
        new_fields = tuple(mapping.get(field, field) for field in self._fields)
        new_rel = type(self)(Record(*new_fields))
        for record in self:
            new_rel.add(new_rel._record_class(*record))
        return new_rel

    def project(self, projection):
        assert set(projection).issubset(self._record_class._fields)
        new_rel = type(self)(Record(*projection))
        for record in self:
            new_rel.add(**dict((field, getattr(record, field)) for field in projection))
        return new_rel

    def display(self):
        """
        Display the relation in tabular form.
        """

        # if it seems inefficient that display uses self.tuples() rather than
        # self.tuples_, it is because that way it will work on views where
        # tuples() is dynamic

        columns = range(len(self._record_class._fields))

        col_width = [len(self._record_class._fields[col]) for col in columns]

        for record in self:
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

        for record in self:
            print line([record._asdict()[self._record_class._fields[col]] for col in columns])

        print hline
