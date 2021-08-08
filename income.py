import argparse


# utils
def lakh(x):
    return x * 10**5

def crore(x):
    return x * 10**7


class Income(object):
    ess = lakh(1.5)
    standard = lakh(0.5)

    def __init__ (self, gross, metro_city=True):
        self.gross = gross

        self.pf = gross * 0.12
        self.basic = gross * 0.5
        self.hra = self.basic * 0.5 if metro_city else self.basic * 0.4

    def taxable(self):
        taxable = self.gross - (self.pf + self.hra + self.ess + self.standard)
        return taxable if taxable > 0 else 0

    def show_income(self):
        tax = self._get_tax()
        if tax:
            tax += self._get_cess(tax) # wtf, tax on tax
            print(f"Gross:                               {int(self.gross):,}")
            print(f"Total Tax to be paid:                {int(tax):,}")
            print("-----------------------------------")
            print(f"Max income possible:                 {int(self.gross - tax):,}")
            print("-----------------------------------")
            print(f"Max in-hand possible:                {int(self.gross - (tax + self.pf)):,}")
            print("-----------------------------------")
            print(f"Max Monthly in-hand possible:        {int((self.gross - (tax + self.pf))/12):,}")
            print("-----------------------------------")

    def _get_tax(self):
        income = self.taxable()
        tax = 0

        if income < lakh(5): # tax exempted by govt
            return 0

        # 5% slab
        tax += lakh(2.5) * 0.05

        # 20% slab
        if income < lakh(10):
            return tax + (income - lakh(5)) * 0.2
        tax += lakh(5) * 0.2

        # 30% slab
        if income < lakh(50):
            return tax + (income - lakh(10)) * 0.3
        tax += lakh(40) * 0.3

        # 10% surcharge
        if income < crore(1):
            return tax + (income - lakh(50)) * 0.1

        if income > crore(1):
            print("you should hire a CA")


    def _get_cess(self, tax):
        return tax * 0.04


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculates your taxes and in hand income')
    parser.add_argument('-s','--salary', help='Annual Salary', required=True)
    parser.add_argument('-m','--metro', help='Do you stay in a metro city, write yes if you do', required=False)
    args = vars(parser.parse_args())
    metro =  args.get('metro') and args['metro'].lower() in {'yes', 'y'}

    i = Income(float(args['salary']), metro)
    i.show_income()
