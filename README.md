# PythonDB
PythonDB is a lightweight document oriented database optimized for your happiness :) It's written in pure Python and with json external dependencies. The target are small apps, script and report that would be blown away by a SQL-DB or an external database server.

# Requirement
- Python 2.7 or higher
- json package

# Example Code
```python
>>> from pythondb import PythonDB
>>> db = PythonDB()
>>> table_name = 'amendment'
>>> db.addTable(table_name)
>>> db.insert(table_name = table_name, values = {"loan_id" : "52152"})
```
 
# Query Language
```python
>>> #Search for a field value
>>> db.select(table_name = table_name, condition = {"loan_id" : ">:52152"})
[{'loan_id': '52152'}]
>>> #Combine two queries with logical and
>>> db.select(table_name = table_name, condition = {"loan_id" : ">:52152", "amendment" : {"status" : str(0)}})

>>> #Combine two queries with logical or
>>> db.select(table_name = table_name, condition = {"or" : {"loan_id" : str(52153), "amendment" : {"status" : str(1)}} }, structure = {})
[{'loan_id': '52152', 'amendment': {'status': '1', 'flag': '3', 'reporting_date': '2017-01-02'}}]

>>> #Combine two queries with logical and(&) and or(|)
>>> db.select(table_name = table_name, condition = {"or" : {"loan_id" : str(52153), "amendment" : {"status" : str(1)}}, "and" : {"amendment" : {"flag" : str(">=:A")}} }, structure = {})
[{'loan_id': '52252', 'amendment': {'status': '1', 'flag': 'A', 'reporting_date': '2017-01-03'}}]

>>> # More possible comparisons:  !=  <  >  <=  >=
```

# Tables
```python
>>> table_name = 'amendment'
>>> db.addTable(table_name)
>>> db.insert(table_name = table_name, values = {"loan_id" : "52152"})
```

# Contributing
Whether reporting bugs, discussing improvements and new ideas or writing extensions: Contributions to PythonDB are welcome!
