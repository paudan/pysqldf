import pandas as pd
from pandasql import SQLDF, load_meat
import string
import unittest


class PandaSQLTest(unittest.TestCase):

    def setUp(self):
        return

    def test_select(self):
        df = pd.DataFrame({
                 "letter_pos": [i for i in range(len(string.ascii_letters))],
                 "l2": list(string.ascii_letters)
        })
        result = SQLDF(locals()).execute("select * from df LIMIT 10;")
        self.assertEqual(len(result), 10)

    def test_join(self):

        df = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "l2": list(string.ascii_letters)
        })

        df2 = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "letter": list(string.ascii_letters)
        })

        result = SQLDF(locals()).execute("SELECT a.*, b.letter FROM df a INNER JOIN df2 b ON a.l2 = b.letter LIMIT 20;")
        self.assertEqual(len(result), 20)

    def test_query_with_spacing(self):

        df = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "l2": list(string.ascii_letters)
        })

        df2 = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "letter": list(string.ascii_letters)
        })

        result = SQLDF(locals()).execute("SELECT a.*, b.letter FROM df a INNER JOIN df2 b ON a.l2 = b.letter LIMIT 20;")
        self.assertEqual(len(result), 20)

        q = """
            SELECT
            a.*
        FROM
            df a
        INNER JOIN
            df2 b
        on a.l2 = b.letter
        LIMIT 20
        ;"""
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 20)

    def test_query_single_list(self):

        mylist = [i for i in range(10)]

        result = SQLDF(locals()).execute("SELECT * FROM mylist")
        self.assertEqual(len(result), 10)

    def test_query_list_of_lists(self):

        mylist = [[i for i in range(10)], [i for i in range(10)]]

        result = SQLDF(locals()).execute("SELECT * FROM mylist")
        self.assertEqual(len(result), 2)

    def test_query_list_of_tuples(self):

        mylist = [tuple([i for i in range(10)]), tuple([i for i in range(10)])]

        result = SQLDF(locals()).execute("SELECT * FROM mylist")
        self.assertEqual(len(result), 2)

    def test_subquery(self):
        kermit = pd.DataFrame({"x": range(10)})
        q = "select * from (select * from kermit) tbl limit 2;"
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 2)

    def test_in(self):
        courseData = {
            'courseCode': ['TM351','TU100','M269'],
            'points':[30,60,30],
            'level':['3','1','2']
        }
        course_df = pd.DataFrame(courseData)
        q = "SELECT * FROM course_df WHERE courseCode IN ( 'TM351', 'TU100' );"
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 2)

    def test_in_with_subquery(self):
        programData = {
            'courseCode': ['TM351','TM351','TM351','TU100','TU100','TU100','M269','M269','M269'],
            'programCode':['AB1','AB2','AB3','AB1','AB3','AB4','AB3','AB4','AB5']
             }
        program_df = pd.DataFrame(programData)

        courseData = {
            'courseCode': ['TM351','TU100','M269'],
            'points':[30,60,30],
            'level':['3','1','2']
        }
        course_df = pd.DataFrame(courseData)

        q = '''
            SELECT * FROM course_df WHERE courseCode IN ( SELECT DISTINCT courseCode FROM program_df ) ;
          '''
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 3)

    def test_datetime_query(self):
        pysqldf = lambda q: sqldf(q, globals())
        meat = load_meat()
        result = SQLDF(locals()).execute("SELECT * FROM meat LIMIT 10;")
        self.assertEqual(len(result), 10)

    def test_returning_none(self):
        pysqldf = lambda q: sqldf(q, globals())
        meat = load_meat()
        result = SQLDF(locals()).execute("SELECT beef FROM meat LIMIT 10;")
        self.assertEqual(len(result), 10)

    def test_nested_list(self):
        data = [[1,2,3], [4,5,6]]
        q = 'select * from data'
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), ['c0', 'c1', 'c2'])
        self.assertEqual(list(result.index), [0, 1])

    def test_list_of_tuple(self):
        data = [(1,2,3), (4,5,6)]
        q = 'select * from data'
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), ['c0', 'c1', 'c2'])
        self.assertEqual(list(result.index), [0, 1])

    def test_list_of_dict(self):
        data = [{"a":1, "b":2, "c":3}, {"a":4, "b":5, "c":6}]
        q = 'select * from data'
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), ['a', 'b', 'c'])
        self.assertEqual(list(result.index), [0, 1])


if __name__=="__main__":
    unittest.main()

