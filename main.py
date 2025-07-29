class Payer:
    def __init__(self):
        self.jobs = []
        self.status = None
        self.deduct = []
        self.rcredit = []
        self.nrcredit = []
        self.standard_deduction_added = False

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
        elif not salary and periods > 0:  # Hourly paycheck
            self.jobs.append((desc, salary, amount, periods, hours))
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
        # Check if this is the standard deduction
        if desc.lower().find('standard') != -1 or amount in [15000, 22500, 30000]:
            self.standard_deduction_added = True

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
        if 0 <= index < len(self.rcredit):
            self.rcredit.pop(index)
            return True
        return False

    def remove_nrcredit(self, index):
        if 0 <= index < len(self.nrcredit):
            self.nrcredit.pop(index)
            return True
        return False

    def calculate_fica(self, gross_income):
        """Calculate FICA taxes (Social Security and Medicare)"""
        # Social Security tax: 6.2% on first $176,100 (2025 limit)
        social_security_limit = 176100
        social_security_tax = min(gross_income, social_security_limit) * 0.062
        
        # Medicare tax: 1.45% on all income
        medicare_tax = gross_income * 0.0145
        
        # Additional Medicare surtax: 0.9% on earnings over threshold
        if self.status == 'U' or self.status == 'H':  # Single or Head of household
            surtax_threshold = 200000
        elif self.status == 'J':  # Married filing jointly
            surtax_threshold = 250000
        elif self.status == 'S':  # Married filing separately
            surtax_threshold = 125000
        else:
            surtax_threshold = 200000  # Default to single threshold
        
        if gross_income > surtax_threshold:
            medicare_surtax = (gross_income - surtax_threshold) * 0.009
            medicare_tax += medicare_surtax
        
        return social_security_tax + medicare_tax

    def calculate_income_tax(self, taxable_income):
        """Calculate federal income tax using 2025 brackets"""
        if self.status == 'U':  # Single
            brackets = [
                (0, 11925, 0.10),
                (11925, 48475, 0.12),
                (48475, 103350, 0.22),
                (103350, 197300, 0.24),
                (197300, 250525, 0.32),
                (250525, 626350, 0.35),
                (626350, float('inf'), 0.37)
            ]
        elif self.status == 'J':  # Married filing jointly
            brackets = [
                (0, 23850, 0.10),
                (23850, 96950, 0.12),
                (96950, 206700, 0.22),
                (206700, 394600, 0.24),
                (394600, 501050, 0.32),
                (501050, 751600, 0.35),
                (751600, float('inf'), 0.37)
            ]
        elif self.status == 'S':  # Married filing separately
            brackets = [
                (0, 11925, 0.10),
                (11925, 48475, 0.12),
                (48475, 103350, 0.22),
                (103350, 197300, 0.24),
                (197300, 250525, 0.32),
                (250525, 375800, 0.35),
                (375800, float('inf'), 0.37)
            ]
        elif self.status == 'H':  # Head of household
            brackets = [
                (0, 17000, 0.10),
                (17000, 64850, 0.12),
                (64850, 103350, 0.22),
                (103350, 197300, 0.24),
                (197300, 250500, 0.32),
                (250500, 626350, 0.35),
                (626350, float('inf'), 0.37)
            ]
        else:
            return 0

        tax = 0
        for i, (lower, upper, rate) in enumerate(brackets):
            if taxable_income > lower:
                if i == len(brackets) - 1:  # Top bracket
                    tax += (taxable_income - lower) * rate
                else:
                    bracket_income = min(taxable_income, upper) - lower
                    tax += bracket_income * rate

        return tax

    def calculate(self):
        """Calculate total tax burden"""
        # Calculate gross income
        gross_income = 0.0
        for job in self.jobs:
            if len(job) == 4:  # Salaried job: (desc, salary, amount, periods)
                desc, salary, amount, periods = job
                if salary:  # Salaried job
                    gross_income += amount * periods
            elif len(job) == 5:  # Hourly job: (desc, salary, amount, periods, hours)
                desc, salary, amount, periods, hours = job
                if not salary:  # Hourly job
                    # Calculate annual income: hourly rate * hours per period * number of periods
                    gross_income += amount * hours * periods  # amount is hourly rate, hours per period, periods per year

        # Calculate FICA taxes
        fica_tax = self.calculate_fica(gross_income)

        # Calculate taxable income
        if self.status == 'J':
            standard_deduction = 30000
        elif self.status == 'H':
            standard_deduction = 22500
        elif self.status == 'S':
            standard_deduction = 15000
        else:  # Single
            standard_deduction = 15000

        taxable_income = gross_income - standard_deduction
        
        # Subtract additional deductions
        for _, amount in self.deduct:
            taxable_income -= amount
        
        taxable_income = max(taxable_income, 0.0)

        # Calculate income tax
        income_tax = self.calculate_income_tax(taxable_income)

        # Apply non-refundable credits
        for _, amount in self.nrcredit:
            income_tax = max(income_tax - amount, 0)

        # Apply refundable credits
        refundable_credit_total = sum(amount for _, amount in self.rcredit)

        # Calculate total tax burden
        total_tax = fica_tax + income_tax - refundable_credit_total

        return {
            'gross_income': gross_income,
            'taxable_income': taxable_income,
            'fica_tax': fica_tax,
            'income_tax': income_tax,
            'refundable_credits': refundable_credit_total,
            'total_tax': total_tax
        }

    def display_jobs(self):
        """Display all jobs with indices"""
        if not self.jobs:
            print("No jobs added yet.")
            return
        
        print("\nCurrent Jobs:")
        for i, job in enumerate(self.jobs):
            if len(job) == 4:  # Salaried job: (desc, salary, amount, periods)
                desc, salary, amount, periods = job
                if salary:
                    print(f"{i}: {desc} - ${amount:,.2f} ({periods} periods)")
            elif len(job) == 5:  # Hourly job: (desc, salary, amount, periods, hours)
                desc, salary, amount, periods, hours = job
                if not salary:
                    print(f"{i}: {desc} - ${amount:.2f}/hour ({hours} hours)")

    def display_deductions(self):
        """Display all deductions with indices"""
        if not self.deduct:
            print("No deductions added yet.")
            return
        
        print("\nCurrent Deductions:")
        for i, (desc, amount) in enumerate(self.deduct):
            print(f"{i}: {desc} - ${amount:,.2f}")

    def display_credits(self, credit_type):
        """Display all credits of specified type with indices"""
        credits = self.rcredit if credit_type == 'refundable' else self.nrcredit
        credit_name = "Refundable Credits" if credit_type == 'refundable' else "Non-refundable Credits"
        
        if not credits:
            print(f"No {credit_name.lower()} added yet.")
            return
        
        print(f"\nCurrent {credit_name}:")
        for i, (desc, amount) in enumerate(credits):
            print(f"{i}: {desc} - ${amount:,.2f}")


def main():
    print("Welcome to the U.S. Federal Personal Income Tax Calculator!")
    print("This calculator uses 2025 tax brackets and rates.")
    
    payer = Payer()
    
    while True:
        print("\n" + "="*50)
        print("MENU:")
        print("1. Add a new job")
        print("2. Add a tax deduction")
        print("3. Add a refundable tax credit")
        print("4. Add a non-refundable tax credit")
        print("5. Set filing status")
        print("6. Remove a job")
        print("7. Remove a tax deduction")
        print("8. Remove a refundable tax credit")
        print("9. Remove a non-refundable tax credit")
        print("10. View all information")
        print("11. Calculate tax burden")
        print("12. Quit")
        print("="*50)
        
        try:
            choice = input("Enter your choice (1-12): ").strip()
            
            if choice == '1':  # Add job
                desc = input("Enter job description: ").strip()
                salary_type = input("Is this a salaried job? (y/n): ").strip().lower()
                
                if salary_type == 'y':
                    print("Period options:")
                    print("A - Annual")
                    print("M - Monthly") 
                    print("S - Semi-monthly")
                    print("B - Bi-weekly")
                    print("W - Weekly")
                    period = input("Enter period (A/M/S/B/W): ").strip().upper()
                    
                    if payer.period_to_number(period) == -1:
                        print("Invalid period. Job not added.")
                        continue
                    
                    try:
                        amount = float(input(f"Enter salary for this {period} period: $"))
                        if payer.add_job(desc, True, amount, period):
                            print("Job added successfully!")
                        else:
                            print("Invalid input. Job not added.")
                    except ValueError:
                        print("Invalid amount. Job not added.")
                else:
                    try:
                        hourly_rate = float(input("Enter hourly rate: $"))
                        
                        print("Period options:")
                        print("A - Annual")
                        print("M - Monthly") 
                        print("S - Semi-monthly")
                        print("B - Bi-weekly")
                        print("W - Weekly")
                        period = input("Enter period (A/M/S/B/W): ").strip().upper()
                        
                        if payer.period_to_number(period) == -1:
                            print("Invalid period. Job not added.")
                            continue
                        
                        hours = float(input("Enter hours worked: "))
                        if payer.add_job(desc, False, hourly_rate, period, hours):
                            print("Job added successfully!")
                        else:
                            print("Invalid input. Job not added.")
                    except ValueError:
                        print("Invalid input. Job not added.")
            
            elif choice == '2':  # Add deduction
                # Check if standard deduction has been added
                if not payer.standard_deduction_added and payer.status:
                    print("\nNote: You haven't added the standard deduction yet.")
                    add_standard = input("Would you like to add the standard deduction now? (y/n): ").strip().lower()
                    if add_standard == 'y':
                        desc = "Standard Deduction"
                        # Standard deduction amounts for 2025
                        if payer.status == 'J':  # Married filing jointly
                            amount = 30000
                        elif payer.status == 'H':  # Head of household
                            amount = 22500
                        elif payer.status == 'S':  # Married filing separately
                            amount = 15000
                        else:  # Single
                            amount = 15000
                        payer.add_deduct(desc, amount)
                        print(f"Standard deduction of ${amount:,.2f} added automatically.")
                        continue
                    elif add_standard == 'n':
                        # User chose not to add standard deduction, continue with regular deduction
                        pass
                    else:
                        print("Invalid input. Please try again.")
                        continue
                elif not payer.status:
                    print("Please set your filing status first (option 5).")
                    continue
                
                # Regular deduction input (only if standard deduction is already added or user chose not to add it)
                desc = input("Enter deduction description: ").strip()
                try:
                    amount = float(input("Enter deduction amount: $"))
                    payer.add_deduct(desc, amount)
                    print("Deduction added successfully!")
                except ValueError:
                    print("Invalid amount. Deduction not added.")
            
            elif choice == '3':  # Add refundable credit
                desc = input("Enter credit description: ").strip()
                try:
                    amount = float(input("Enter credit amount: $"))
                    payer.add_rcredit(desc, amount)
                    print("Refundable credit added successfully!")
                except ValueError:
                    print("Invalid amount. Credit not added.")
            
            elif choice == '4':  # Add non-refundable credit
                desc = input("Enter credit description: ").strip()
                try:
                    amount = float(input("Enter credit amount: $"))
                    payer.add_nrcredit(desc, amount)
                    print("Non-refundable credit added successfully!")
                except ValueError:
                    print("Invalid amount. Credit not added.")
            
            elif choice == '5':  # Set filing status
                print("Filing Status Options:")
                print("U - Unmarried (Single)")
                print("J - Joint and married")
                print("S - Separate and married")
                print("H - Head of household")
                status = input("Enter filing status (U/J/S/H): ").strip().upper()
                if payer.set_status(status):
                    print("Filing status set successfully!")
                else:
                    print("Invalid filing status.")
            
            elif choice == '6':  # Remove job
                payer.display_jobs()
                if payer.jobs:
                    try:
                        index = int(input("Enter job index to remove: "))
                        if payer.remove_job(index):
                            print("Job removed successfully!")
                        else:
                            print("Invalid index.")
                    except ValueError:
                        print("Invalid index.")
            
            elif choice == '7':  # Remove deduction
                payer.display_deductions()
                if payer.deduct:
                    try:
                        index = int(input("Enter deduction index to remove: "))
                        if payer.remove_deduct(index):
                            print("Deduction removed successfully!")
                        else:
                            print("Invalid index.")
                    except ValueError:
                        print("Invalid index.")
            
            elif choice == '8':  # Remove refundable credit
                payer.display_credits('refundable')
                if payer.rcredit:
                    try:
                        index = int(input("Enter credit index to remove: "))
                        if payer.remove_rcredit(index):
                            print("Refundable credit removed successfully!")
                        else:
                            print("Invalid index.")
                    except ValueError:
                        print("Invalid index.")
            
            elif choice == '9':  # Remove non-refundable credit
                payer.display_credits('non-refundable')
                if payer.nrcredit:
                    try:
                        index = int(input("Enter credit index to remove: "))
                        if payer.remove_nrcredit(index):
                            print("Non-refundable credit removed successfully!")
                        else:
                            print("Invalid index.")
                    except ValueError:
                        print("Invalid index.")
            
            elif choice == '10':  # View all information
                print("\n" + "="*50)
                print("CURRENT INFORMATION")
                print("="*50)
                
                # Filing status
                status_names = {
                    'U': 'Single',
                    'J': 'Married Filing Jointly', 
                    'S': 'Married Filing Separately',
                    'H': 'Head of Household'
                }
                if payer.status:
                    print(f"Filing Status: {status_names.get(payer.status, 'Unknown')}")
                else:
                    print("Filing Status: Not set")
                
                # Jobs
                if payer.jobs:
                    print(f"\nJobs ({len(payer.jobs)}):")
                    for i, job in enumerate(payer.jobs):
                        if len(job) == 4:  # Salaried job: (desc, salary, amount, periods)
                            desc, salary, amount, periods = job
                            if salary:
                                print(f"  {i+1}. {desc} - ${amount:,.2f} ({periods} periods)")
                        elif len(job) == 5:  # Hourly job: (desc, salary, amount, periods, hours)
                            desc, salary, amount, periods, hours = job
                            if not salary:
                                print(f"  {i+1}. {desc} - ${amount:.2f}/hour ({hours} hours, {periods} periods)")
                else:
                    print("\nJobs: None added")
                
                # Deductions
                if payer.deduct:
                    print(f"\nDeductions ({len(payer.deduct)}):")
                    for i, (desc, amount) in enumerate(payer.deduct):
                        print(f"  {i+1}. {desc} - ${amount:,.2f}")
                else:
                    print("\nDeductions: None added")
                
                # Refundable credits
                if payer.rcredit:
                    print(f"\nRefundable Credits ({len(payer.rcredit)}):")
                    for i, (desc, amount) in enumerate(payer.rcredit):
                        print(f"  {i+1}. {desc} - ${amount:,.2f}")
                else:
                    print("\nRefundable Credits: None added")
                
                # Non-refundable credits
                if payer.nrcredit:
                    print(f"\nNon-refundable Credits ({len(payer.nrcredit)}):")
                    for i, (desc, amount) in enumerate(payer.nrcredit):
                        print(f"  {i+1}. {desc} - ${amount:,.2f}")
                else:
                    print("\nNon-refundable Credits: None added")
                
                # Standard deduction status
                if payer.standard_deduction_added:
                    print("\nStandard Deduction: Added")
                else:
                    print("\nStandard Deduction: Not added")
                
                print("="*50)
            
            elif choice == '11':  # Calculate tax burden
                if not payer.status:
                    print("Please set your filing status first (option 5).")
                    continue
                
                if not payer.jobs:
                    print("Please add at least one job first (option 1).")
                    continue
                
                result = payer.calculate()
                
                print("\n" + "="*50)
                print("TAX CALCULATION RESULTS")
                print("="*50)
                print(f"Gross Income: ${result['gross_income']:,.2f}")
                print(f"Taxable Income: ${result['taxable_income']:,.2f}")
                print(f"FICA Taxes: ${result['fica_tax']:,.2f}")
                print(f"Federal Income Tax: ${result['income_tax']:,.2f}")
                print(f"Refundable Credits: ${result['refundable_credits']:,.2f}")
                print("-" * 50)
                print(f"Total Tax Burden: ${result['total_tax']:,.2f}")
                print("="*50)
            
            elif choice == '12':  # Quit
                print("Thank you for using the tax calculator!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 12.")
        
        except KeyboardInterrupt:
            print("\n\nThank you for using the tax calculator!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
