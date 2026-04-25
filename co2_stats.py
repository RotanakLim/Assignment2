import csv
from typing import *
from dataclasses import dataclass
import unittest
import math
import sys
sys.setrecursionlimit(10**6)

@dataclass (frozen=True)
class Row:
  country:str
  year:int
  emissions:float

RLList: TypeAlias = Optional['RLNode']

@dataclass(frozen=True)
class RLNode:
  first:Row
  rest: RLList

rows: RLList = None

#Reads the 'filename' and returns a linked list of row objects
def read_csv_lines(filename:str) -> RLList:
  rows = None
  f = open(filename)
  reader = csv.reader(f)
  next(reader)
  temp_rows: List[Row] = []
  for line in reader:
    temp_rows.append(helper_function(line))
  f.close()

  for row in reversed(temp_rows):
    rows = RLNode(row, rows)

  return rows

#takes a list of strings 'fields' and returns a row object with the country, year, and emissions values
def helper_function(fields: list[str]) -> Row:
  return Row(
    country=fields[0],
    year=int(fields[1]),
    emissions=float(fields[2])
  )

#"Some questions" question 2
#Takes rows where the country is Mexico and returns a linked list
def mexico_rows(rows: RLList) -> RLList:
  if rows is None:
    return None
  else:
    rest_result = mexico_rows(rows.rest)
    if rows.first.country == "Mexico":
      return RLNode(rows.first, rest_result)
    else:
      return rest_result

#question 3
#Takes rows and returns the emissions value for the United States in 1990
def us_1990_emissions(rows: RLList) -> RLList:
  if rows is None:
    return 0.0
  if rows.first.country == "United States" and rows.first.year == 1990:
    return rows.first.emissions
  return us_1990_emissions(rows.rest)

#takes rows and returns a linked list of rows where the emissions are greater than the untied stated emissions during 1990
def higher_than_us_1990(rows: RLList, us_value: float= None) -> RLList:
  if rows is None:
    return None
  if us_value is None:
    us_value = us_1990_emissions(rows)
  rest_result = higher_than_us_1990(rows.rest, us_value)
  if rows.first.emissions > us_value:
    return RLNode(rows.first, rest_result)
  else:
    return rest_result
#Question 4
#takes rows and returns a linked list of Rows with emissions greater than United States in 2020
def higher_than_us_2020(rows: RLList) -> RLList:
  us_value = higher_than_us_2020_helper(rows, 0.0, True)
  return higher_than_us_2020_helper(rows, us_value, False)

#takes rows, us_value, and finding_us and either finds the us 202 emissions or returns rows with emissions greater than the US value
def higher_than_us_2020_helper(rows: RLList, us_value: float, finding_us: bool):
  if rows is None:
    if finding_us:
      return 0.0
    else:
      return None
  if finding_us:
    if rows.first.country == "United States" and rows.first.year == 2020:
      return rows.first.emissions
    return higher_than_us_2020_helper(rows.rest, us_value, True)
  else:
    rest_result = higher_than_us_2020_helper(rows.rest, us_value, False)
    if rows.first.emissions > us_value:
      return RLNode(rows.first, rest_result)
    else:
      return rest_result



class Tests(unittest.TestCase):

  def test_read_csv_lines_first(self) -> None:
    result = read_csv_lines("sample-file.csv")
    assert result.first == Row("Lithuania", 1994, 7.27)

  def test_read_csv_lines_second(self) -> None:
    result = read_csv_lines("sample-file.csv")
    assert result.rest.first == Row("Lithuania", 1995, 6.41)

  def test_helper_function_1(self) -> None:
    assert helper_function(["Canada", "2020", "15.5"]) == Row("Canada", 2020, 15.5)


  def test_helper_function_2(self) -> None:
    assert helper_function(["Brazil", "1999", "42.0"]) == Row("Brazil", 1999, 42.0)

  def test_mexico_rows_first(self) -> None:
    rows = RLNode(Row("Mexico", 1991, 106.6),
           RLNode(Row("Canada", 2020, 15.5), None))
    result = mexico_rows(rows)
    assert result.first == Row("Mexico", 1991, 106.6)

  def test_mexico_rows_second(self) -> None:
    rows = RLNode(Row("Brazil", 2000, 20.0),
           RLNode(Row("Mexico", 1992, 107.57),
           RLNode(Row("Mexico", 1993, 114.18), None)))
    result = mexico_rows(rows)
    assert result.first == Row("Mexico", 1992, 107.57)

  def test_us_1990_emissions_found(self) -> None:
    rows = RLNode(Row("Canada", 1990, 5.0),
                  RLNode(Row("United States", 1990, 20.0), None))
    assert us_1990_emissions(rows) == 20.0

  def test_us_1990_emissions_not_found(self) -> None:
    rows = RLNode(Row("Canada", 1990, 5.0), None)
    assert us_1990_emissions(rows) == 0.0

  def test_higher_than_us_1990_one(self) -> None:
    rows = RLNode(Row("United States", 1990, 10.0),
                  RLNode(Row("Canada", 1990, 15.0), None))
    result = higher_than_us_1990(rows)
    assert result.first == Row("Canada", 1990, 15.0)

  def test_higher_than_us_1990_none(self) -> None:
    rows = RLNode(Row("United States", 1990, 20.0),
                  RLNode(Row("Canada", 1990, 10.0), None))
    result = higher_than_us_1990(rows)
    assert result is None

  def test_higher_than_us_2020_one(self) -> None:
    rows = RLNode(Row("United States", 2020, 10.0),
           RLNode(Row("Canada", 2020, 15.0), None))
    result = higher_than_us_2020(rows)
    assert result.first == Row("Canada", 2020, 15.0)
    assert result.rest is None

  def test_higher_than_us_2020_none(self) -> None:
    rows = RLNode(Row("United States", 2020, 20.0),
                  RLNode(Row("Canada", 2020, 10.0), None))
    result = higher_than_us_2020(rows)
    assert result is None

if (__name__ == '__main__'):
  unittest.main()
