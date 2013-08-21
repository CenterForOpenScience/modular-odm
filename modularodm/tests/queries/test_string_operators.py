import datetime as dt
import os
import unittest


from modularodm import fields, StoredObject
from modularodm.query.query import RawQuery as Q
from modularodm.storage import PickleStorage


class StringComparisonPickleTestCase(unittest.TestCase):

    make_storage = lambda x: PickleStorage('Test')

    def setUp(self):
        super(StringComparisonPickleTestCase, self).setUp()
        self.set_up_objects()

    def tearDown(self):
        self.tear_down_objects()
        super(StringComparisonPickleTestCase, self).tearDown()

    def set_up_objects(self):
        class Foo(StoredObject):
            _id = fields.IntegerField(primary=True)
            string_field = fields.StringField()

        Foo.set_storage(self.make_storage())
        Foo._clear_caches()

        self.Foo = Foo
        self.foos = []

        field_values = (
            'first value',
            'second value',
            'third value',
        )

        for idx in xrange(len(field_values)):
            foo = Foo(
                _id=idx,
                string_field=field_values[idx],
            )
            foo.save()
            self.foos.append(foo)

    def tear_down_objects(self):
        try:
            os.remove('db_Test.pkl')
        except OSError:
            pass

    def test_contains(self):
        """ Finds objects with the attribute containing the substring."""
        result = self.Foo.find(
            Q('string_field', 'contains', 'second')
        )
        self.assertEqual(len(result), 1)

    def test_icontains(self):
        """ Operates as ``contains``, but ignores case."""
        result = self.Foo.find(
            Q('string_field', 'icontains', 'SeCoNd')
        )
        self.assertEqual(len(result), 1)

    def test_startwith(self):
        """ Finds objects where the attribute begins with the substring """
        result = self.Foo.find(
            Q('string_field', 'startswith', 'second')
        )
        self.assertEqual(len(result), 1)

    def test_endswith(self):
        """ Finds objects where the attribute ends with the substring """
        result = self.Foo.find(
            Q('string_field', 'endswith', 'value')
        )
        self.assertEqual(len(result), 3)


# TODO: The following are defined in MongoStorage, but not PickleStorage:
#   'istartswith'
#   'iendswith',
#   'exact',
#   'iexact'


# TODO: MongoStorageTestCase not yet implemented
# class StringComparisonMongoTestCase(BasicQueryBase, MongoStorageTestCase):
#     pass