from functools import update_wrapper

import exchequer
from urecord import Record


def union_compatible(method):
    """Declare a set operation as requiring union-compatibility."""

    def wrapper(self, other_rel):
        assert self._record_class._fields == other_rel._record_class._fields
        result = method(self, other_rel)
        result._record_class = self._record_class
        return result
    try:
        update_wrapper(wrapper, method)
    except Exception:
        pass
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

    def display(self, outfile=None, encoding='utf-8'):
        """
        Display the relation in tabular form.

        This method uses Exchequer (http://zacharyvoase.github.com/exchequer/)
        to format the output table. Pass `outfile` if you want to write to
        another file-like object (such as stderr or a StringIO). `encoding`
        will be used when handling bytestrings in your records.
        """

        exchequer.print_table([self._record_class._fields] + list(self),
                outfile=outfile, encoding=encoding)
