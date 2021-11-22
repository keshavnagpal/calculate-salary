# calculate-salary

Command line script to calculate taxes and in hand salary

## Usage

```
usage: python3 income.py [-h] -s SALARY [-m METRO] [-pf PF]

Calculates your taxes and in hand income

optional arguments:
  -h, --help            show this help message and exit
  -s SALARY, --salary SALARY
                        Annual Salary
  -m METRO, --metro METRO
                        'yes' if you stay in a metro city, 'no' otherwise
  -pf PF                'yes' if your pf is inclusive in the salary mentioned, 'no' otherwise
```

## Note:

- Script Assumes Deductions under 80C, 80D, Section 10(13A) in old tax regime
- No deductions are allowed in new tax regime (only employer pf is deducted if it is inclusive in salary)
- To know more about income-tax slabs go to [income-tax-india](https://www.incometaxindia.gov.in/_layouts/15/dit/mobile/viewer.aspx?path=https://www.incometaxindia.gov.in/charts++tables/tax+rates.htm&k&IsDlg=0)
