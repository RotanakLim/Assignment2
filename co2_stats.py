import csv
from typing import Optional, TypeAlias, Literal
from dataclasses import dataclass
import unittest
import math
import sys


sys.setrecursionlimit(10 ** 6)




@dataclass(frozen=True)
class Row:
   country: str
   year: int
   electricity_and_heat_co2_emissions: float
   electricity_and_heat_co2_emissions_per_capita: float
   energy_co2_emissions: float
   energy_co2_emissions_per_capita: float
   total_co2_emissions_excluding_lucf: float
   total_co2_emissions_excluding_lucf_per_capita: float




RLList: TypeAlias = Optional["RLNode"]




@dataclass(frozen=True)
class RLNode:
   first: Row
   rest: RLList




# takes a list of strings 'fields' and returns a row object with the country, year, and emissions values
def helper_function(fields: list[str]) -> Row:
   return Row(
       country=fields[0],
       year=int(fields[1]),
       electricity_and_heat_co2_emissions=float(fields[2]),
       electricity_and_heat_co2_emissions_per_capita=float(fields[3]),
       energy_co2_emissions=float(fields[4]),
       energy_co2_emissions_per_capita=float(fields[5]),
       total_co2_emissions_excluding_lucf=float(fields[6]),
       total_co2_emissions_excluding_lucf_per_capita=float(fields[7])
   )




# Reads the 'filename' and returns a linked list of row objects
def read_csv_lines(filename: str) -> RLList:
   rows: RLList = None
   f = open(filename)
   reader = csv.reader(f)
   next(reader)
   temp_rows: list[Row] = []
   for line in reader:
       temp_rows.append(helper_function(line))
   f.close()


   for row in reversed(temp_rows):
       rows = RLNode(row, rows)


   return rows




# takes in object "R" and return the length
def listlen(rows: RLList) -> int:
   count = 0
   current = rows


   while current is not None:
       count += 1
       current = current.rest


   return count




# takes input field, comparison, and comparison, and produces whether the comparison is true."
def compare(field_value, comparison_type, comparison_value):
   if comparison_type == "less_than":
       return field_value < comparison_value
   elif comparison_type == "equal":
       return field_value == comparison_value
   else:
       return field_value > comparison_value




FieldName = Literal[
   "country",
   "year",
   "electricity_and_heat_co2_emissions",
   "electricity_and_heat_co2_emissions_per_capita",
   "energy_co2_emissions",
   "energy_co2_emissions_per_capita",
   "total_co2_emissions_excluding_lucf",
   "total_co2_emissions_excluding_lucf_per_capita"
]
ComparisonType = Literal["less_than", "equal", "greater_than"]




# takes a input of linked list of Rows, a field, comparison, and produces 'Rows' that matches comparison."
def filter_rows(rows, field_name, comparison_type, comparison_value):
   if field_name == "country" and comparison_type != "equal":
       raise ValueError("Invalid comparison for country")


   if rows is None:
       return None


   rest_result = filter_rows(rows.rest, field_name, comparison_type, comparison_value)
   field_value = getattr(rows.first, field_name)


   if compare(field_value, comparison_type, comparison_value):
       return RLNode(rows.first, rest_result)
   else:
       return rest_result




# question 2
# takes a input 'rows' and produces the number of unique countries in the dataset.
def count_countries(rows: RLList) -> int:
   if rows is None:
       return 0


   target_year = rows.first.year
   count = 0
   current = rows


   while current is not None:
       if current.first.year == target_year:
           count += 1
       current = current.rest


   return count




# "Some questions" question 2
# Takes rows where the country is Mexico and returns a linked list
def mexico_rows(rows: RLList) -> RLList:
   if rows is None:
       return None
   else:
       rest_result = mexico_rows(rows.rest)
       if rows.first.country == "Mexico":
           return RLNode(rows.first, rest_result)
       else:
           return rest_result




# question 3
# Takes rows and returns the emissions value for the United States in 1990
def us_1990_emissions(rows: RLList) -> float:
   if rows is None:
       return 0.0
   if rows.first.country == "United States" and rows.first.year == 1990:
       return rows.first.total_co2_emissions_excluding_lucf_per_capita
   return us_1990_emissions(rows.rest)




# takes rows and returns a linked list of rows where the emissions are greater than the untied stated emissions during 1990
def higher_than_us_1990(rows: RLList, us_value: float = None) -> RLList:
   if rows is None:
       return None
   if us_value is None:
       us_value = us_1990_emissions(rows)
   rest_result = higher_than_us_1990(rows.rest, us_value)
   if rows.first.total_co2_emissions_excluding_lucf_per_capita > us_value:
       return RLNode(rows.first, rest_result)
   else:
       return rest_result




# Question 4
# takes rows and returns a linked list of Rows with emissions greater than United States in 2020
def higher_than_us_2020(rows: RLList) -> RLList:
   us_value = higher_than_us_2020_helper(rows, 0.0, True)
   return higher_than_us_2020_helper(rows, us_value, False)




# takes rows, us_value, and finding_us and either finds the us 202 emissions or returns rows with emissions greater than the US value
def higher_than_us_2020_helper(rows: RLList, us_value: float, finding_us: bool):
   if rows is None:
       if finding_us:
           return 0.0
       else:
           return None
   if finding_us:
       if rows.first.country == "United States" and rows.first.year == 2020:
           return rows.first.total_co2_emissions_excluding_lucf_per_capita
       return higher_than_us_2020_helper(rows.rest, us_value, True)
   else:
       rest_result = higher_than_us_2020_helper(rows.rest, us_value, False)
       if rows.first.total_co2_emissions_excluding_lucf_per_capita > us_value:
           return RLNode(rows.first, rest_result)
       else:
           return rest_result




# question 4
# takes input rows and produces the population of Luxembourg in 2014
def luxembourg_population_2014(rows: RLList) -> float:
   if rows is None:
       return 0.0


   if rows.first.country == "Luxembourg" and rows.first.year == 2014:
       total = rows.first.total_co2_emissions_excluding_lucf
       per_capita = rows.first.total_co2_emissions_excluding_lucf_per_capita
       return (total / per_capita) * 1_000_000


   return luxembourg_population_2014(rows.rest)




#Takes rows and returns the expected emissions for China in 2070 based on the growth from 1990 to 2020
def china_emissions_2070(rows: RLList) -> float:
   china_1990 = 0.0
   china_2020 = 0.0
   current = rows
   while current is not None:
       if current.first.country == "China" and current.first.year == 1990:
           china_1990 = current.first.electricity_and_heat_co2_emissions
       if current.first.country == "China" and current.first.year == 2020:
           china_2020 = current.first.electricity_and_heat_co2_emissions
       current = current.rest
   if china_1990 == 0.0 or china_2020 == 0.0:
       return 0.0
   growth_multiplier = china_2020 / china_1990
   annual_growth = growth_multiplier ** (1 / 30)
   return china_2020 * (annual_growth ** 50)




class Tests(unittest.TestCase):


   def test_read_csv_lines_first(self) -> None:
       result = read_csv_lines("sample-file.csv")
       self.assertEqual(
           result.first,
           Row("Lithuania", 1994, 7.27, 1.9281462, 14.44, 3.8297703, 14.82, 3.930554)
       )


   def test_read_csv_lines_second(self) -> None:
       result = read_csv_lines("sample-file.csv")
       self.assertEqual(
           result.rest.first,
           Row("Lithuania", 1995, 6.41, 1.710579, 13.44, 3.586612, 13.75, 3.669339)
       )


   def test_listlen_empty(self) -> None:
       self.assertEqual(listlen(None), 0)


   def test_listlen_multiple(self) -> None:
       rows = RLNode(
           Row("Mexico", 1991, 106.6, 1.2789197, 277.05, 3.3238711, 288.0, 3.4552426),
           RLNode(
               Row("Canada", 2020, 15.5, 0.5, 100.0, 2.0, 110.0, 2.2),
               RLNode(
                   Row("Brazil", 2000, 20.0, 1.0, 120.0, 3.0, 130.0, 3.5),
                   None
               )
           )
       )
       self.assertEqual(listlen(rows), 3)


   def test_helper_function_1(self) -> None:
       self.assertEqual(
           helper_function(["Canada", "2020", "15.5", "0.5", "100.0", "2.0", "110.0", "2.2"]),
           Row("Canada", 2020, 15.5, 0.5, 100.0, 2.0, 110.0, 2.2)
       )


   def test_helper_function_2(self) -> None:
       self.assertEqual(
           helper_function(["Brazil", "1999", "42.0", "1.5", "150.0", "3.5", "160.0", "4.0"]),
           Row("Brazil", 1999, 42.0, 1.5, 150.0, 3.5, 160.0, 4.0)
       )


   def test_mexico_rows_first(self) -> None:
       rows = RLNode(
           Row("Mexico", 1991, 106.6, 1.2789197, 277.05, 3.3238711, 288.0, 3.4552426),
           RLNode(Row("Canada", 2020, 15.5, 0.5, 100.0, 2.0, 110.0, 2.2), None)
       )
       result = mexico_rows(rows)
       self.assertEqual(
           result.first,
           Row("Mexico", 1991, 106.6, 1.2789197, 277.05, 3.3238711, 288.0, 3.4552426)
       )


   def test_luxembourg_population_found(self) -> None:
       rows = RLNode(
           Row("Luxembourg", 2014, 0.0, 0.0, 0.0, 0.0, 10.0, 2.0),
           None
       )
       self.assertEqual(luxembourg_population_2014(rows), 5_000_000.0)


   def test_luxembourg_population_not_found(self) -> None:
       rows = RLNode(
           Row("Canada", 2014, 0.0, 0.0, 0.0, 0.0, 10.0, 2.0),
           None
       )
       self.assertEqual(luxembourg_population_2014(rows), 0.0)


   def test_mexico_rows_second(self) -> None:
       rows = RLNode(
           Row("Brazil", 2000, 20.0, 1.0, 120.0, 3.0, 130.0, 3.5),
           RLNode(
               Row("Mexico", 1992, 107.57, 1.2656312, 279.93, 3.293559, 291.68, 3.4318056),
               RLNode(
                   Row("Mexico", 1993, 114.18, 1.3177387, 288.28, 3.3270073, 300.67, 3.469999),
                   None
               )
           )
       )
       result = mexico_rows(rows)
       self.assertEqual(
           result.first,
           Row("Mexico", 1992, 107.57, 1.2656312, 279.93, 3.293559, 291.68, 3.4318056)
       )


   def test_us_1990_emissions_found(self) -> None:
       rows = RLNode(
           Row("Canada", 1990, 0.0, 0.0, 0.0, 0.0, 50.0, 5.0),
           RLNode(
               Row("United States", 1990, 0.0, 0.0, 0.0, 0.0, 200.0, 20.0),
               None
           )
       )
       self.assertEqual(us_1990_emissions(rows), 20.0)


   def test_us_1990_emissions_not_found(self) -> None:
       rows = RLNode(Row("Canada", 1990, 0.0, 0.0, 0.0, 0.0, 50.0, 5.0), None)
       self.assertEqual(us_1990_emissions(rows), 0.0)


   def test_higher_than_us_1990_one(self) -> None:
       rows = RLNode(
           Row("United States", 1990, 0.0, 0.0, 0.0, 0.0, 100.0, 10.0),
           RLNode(
               Row("Canada", 1990, 0.0, 0.0, 0.0, 0.0, 150.0, 15.0),
               None
           )
       )
       result = higher_than_us_1990(rows)
       self.assertEqual(result.first, Row("Canada", 1990, 0.0, 0.0, 0.0, 0.0, 150.0, 15.0))


   def test_higher_than_us_1990_none(self) -> None:
       rows = RLNode(
           Row("United States", 1990, 0.0, 0.0, 0.0, 0.0, 200.0, 20.0),
           RLNode(
               Row("Canada", 1990, 0.0, 0.0, 0.0, 0.0, 100.0, 10.0),
               None
           )
       )
       result = higher_than_us_1990(rows)
       self.assertIsNone(result)


   def test_higher_than_us_2020_one(self) -> None:
       rows = RLNode(
           Row("United States", 2020, 0.0, 0.0, 0.0, 0.0, 100.0, 10.0),
           RLNode(
               Row("Canada", 2020, 0.0, 0.0, 0.0, 0.0, 150.0, 15.0),
               None
           )
       )
       result = higher_than_us_2020(rows)
       self.assertEqual(result.first, Row("Canada", 2020, 0.0, 0.0, 0.0, 0.0, 150.0, 15.0))
       self.assertIsNone(result.rest)


   def test_higher_than_us_2020_none(self) -> None:
       rows = RLNode(
           Row("United States", 2020, 0.0, 0.0, 0.0, 0.0, 200.0, 20.0),
           RLNode(
               Row("Canada", 2020, 0.0, 0.0, 0.0, 0.0, 100.0, 10.0),
               None
           )
       )
       result = higher_than_us_2020(rows)
       self.assertIsNone(result)


   def test_china_emissions_2070_basic(self) -> None:
       rows = RLNode(
           Row("China", 1990, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0),
           RLNode(
               Row("China", 2020, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0),
               None
           )
       )
       expected = 20.0 * ((20.0 / 10.0) ** (50 / 30))
       self.assertAlmostEqual(china_emissions_2070(rows), expected)


   def test_china_emissions_2070_no_1990(self) -> None:
       rows = RLNode(
           Row("China", 2020, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0),
           None
       )
       result = china_emissions_2070(rows)
       self.assertEqual(result, 0.0)




if (__name__ == '__main__'):
   unittest.main()



