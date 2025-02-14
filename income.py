import argparse


# utils
def lakh(x):
    return x * 10 ** 5


def crore(x):
    return x * 10 ** 7


class Income(object):
    ess = lakh(1.5)
    standard = lakh(0.5)
    standard_new_regime = lakh(0.75)
    medical = lakh(0.5)

    def __init__(self, gross, metro_city, pf):
        self.gross = gross
        self.basic = gross * 0.5
        self.hra = self.basic * 0.4 if metro_city is False else self.basic * 0.5

        self.pf_employee = self.pf_employer = self.basic * 0.12 if pf else 0
        self.pf = self.pf_employee + self.pf_employer

        # fmt: off
        self.strings = {
            "gross":   "Gross:                               ",
            "tax":     "Total Tax (including cess):          ",
            "income":  "Income possible (cash + pf):         ",
            "monthly": "Monthly (cash + pf):                 ",
            "metro":  f"Metro City:                          {'Yes' if metro_city else 'No'}",
            "pf":     f"PF Inclusive in Salary:              {'Yes' if pf else 'No'}",
        }
        # fmt: on

    def show(self):
        if self.gross > crore(1):
            print("you should hire a CA")
            return

        print(self.strings['metro'])
        print(self.strings['pf'])
        print(f"{self.strings['gross']}{int(self.gross):,}\n")

        print("-----------------Old Regime-------------------")
        self.show_income(self._get_tax_old_regime())
        print("-----------------New Regime-------------------")
        self.show_income(self._get_tax_new_regime())

    def show_income(self, tax):
        mih = self.monthly_in_hand(tax)
        print(f"{self.strings['tax']}{int(tax):,}")
        print("------------------------------------------------")
        print(f"{self.strings['income']}{int(self.gross - tax):,}")
        print("------------------------------------------------")
        print(f"{self.strings['monthly']}{mih + int(self.pf/12):,} ( {mih:,} + {int(self.pf/12):,} )")
        print("------------------------------------------------\n")

    def taxable(self, regime=None):
        if regime == 'new':
            return self.gross - (self.pf / 2) - self.standard_new_regime

        ess = lakh(1.5) if not self.pf_employee else 0
        taxable = self.gross - (self.pf_employer + self.hra + ess + self.standard
                                + self.medical + min(self.pf_employee, lakh(2.5)))
        return taxable if taxable > 0 else 0

    def monthly_in_hand(self, tax):
        if not tax:
            return int((self.gross - self.pf) / 12)

        return int((self.gross - (tax + self.pf)) / 12)

    def _get_tax_old_regime(self):
        income = self.taxable()
        tax = 0

        if income < lakh(5):  # tax exempted by govt
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
        # TODO: include marginal relief
        if income < crore(1):
            return tax + tax * 0.1

        return 0

    def _get_tax_new_regime(self):
        # as per 2023 budget
        income = self.taxable('new')
        tax = 0

        if income < lakh(12):  # tax exempted by govt
            return 0

        # 5% slab 4-8L
        tax += lakh(4) * 0.05
        income -= lakh(4)

        # 10% slab 8-12L
        tax += lakh(4) * 0.1
        income -= lakh(4)

        # 15% slab 12-16L
        if income < lakh(4):
            tax = tax + income * 0.15
            return tax


        tax += lakh(4) * 0.15
        income -= lakh(4)

        # 20% slab 16-20L
        if income < lakh(4):
            tax = tax + income * 0.2
            return tax


        tax += lakh(4) * 0.2
        income -= lakh(4)

        # 25% slab 20-24L
        if income < lakh(4):
            tax = tax + income * 0.25
            return tax


        tax += lakh(4) * 0.25
        income -= lakh(4)

        # 30% slab 24-50L
        if income < lakh(50):
            tax = tax + income * 0.3
            return tax


        tax += lakh(26) * 0.3
        income -= lakh(26)

        # 10% surcharge
        # TODO: include marginal relief
        if income < lakh(50):
            return tax + tax * 0.1

        return 0

    def _get_cess(self, tax):
        # tax on tax
        return tax * 0.04


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculates your taxes and in hand income"
    )
    parser.add_argument("-s", "--salary", help="Annual Salary", required=True)
    parser.add_argument(
        "-m",
        "--metro",
        help="'yes' if you stay in a metro city, 'no' otherwise",
        required=False,
    )
    parser.add_argument(
        "-pf",
        help="'yes' if your pf is inclusive in the salary mentioned, 'no' otherwise",
        required=False,
    )
    args = vars(parser.parse_args())
    metro = (
        False if args.get("metro") and args["metro"].lower() in {"no", "n"} else True
    )
    pf = (
        False if args.get("pf") and args["pf"].lower() in {"no", "n"} else True
    )

    i = Income(float(args["salary"]), metro, pf)
    i.show()
