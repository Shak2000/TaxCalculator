class Payer:
    def __init__(self):
        self.jobs = []
        self.status = None
        self.deduct = []
        self.rcredit = []
        self.nrcredit = []

    def period_to_number(self, period):
        if period == 'A':  # Annual
            return 1
        elif period == 'M':  # Monthly
            return 12
        elif period == 'S':  # Semi-monthly
            return 24
        elif period == 'B':  # Bi-weekly
            return 26
        elif period == 'W':  # Weekly
            return 52
        else:  # Invalid input
            return -1

    def add_job(self, desc, salary, amount, period='A', hours=40):
        periods = self.period_to_number(period)
        if salary and periods > 0:  # Salary paycheck
            self.jobs.append((desc, salary, amount, periods))
            return True
        elif not salary:  # Hourly paycheck
            self.jobs.append((desc, salary, amount, hours))
            return True
        return False

    def remove_job(self, index):
        if 0 <= index < len(self.jobs):
            self.jobs.pop(index)
            return True
        return False

    def set_status(self, status):
        # Unmarried, Joint and married, Separate and married, or Head of household
        if status == 'U' or status == 'J' or status == 'S' or status == 'H':
            self.status = status
            return True
        return False

    def add_deduct(self, desc, amount):
        # Add a tax deduction besides the standard one
        self.deduct.append((desc, amount))

    def add_rcredit(self, desc, amount):
        self.rcredit.append((desc, amount))

    def add_nrcredit(self, desc, amount):
        self.nrcredit.append((desc, amount))

    def remove_deduct(self, index):
        if 0 <= index < len(self.deduct):
            self.deduct.pop(index)
            return True
        return False

    def remove_rcredit(self, index):
        if 0 <= index < len(self.deduct):
            self.rcredit.pop(index)
            return True
        return False

    def remove_nrcredit(self, index):
        if 0 <= index < len(self.deduct):
            self.nrcredit.pop(index)
            return True
        return False

    def calculate(self):
        income = 0.0
        for _, _, amount, periods in self.jobs:
            income += amount * periods

        if self.status == 'J':
            income -= 30000.0
        elif self.status == 'H':
            income -= 22500.0
        else:
            income -= 15000.0
        for _, amount in self.deduct:
            income -= amount
        income = max(income, 0.0)


def main():
    print("Welcome to the tax calculator!")


if __name__ == "__main__":
    main()
