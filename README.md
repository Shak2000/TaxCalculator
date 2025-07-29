# U.S. Federal Personal Income Tax Calculator

A comprehensive tax calculator for the 2025 tax year that helps individuals estimate their federal income tax burden. The application features both a command-line interface and a modern web interface with real-time calculations.

## Features

- **Multiple Interface Options**: Command-line tool and modern web UI
- **Comprehensive Tax Calculations**: 
  - Federal income tax using 2025 tax brackets
  - FICA taxes (Social Security and Medicare)
  - Additional Medicare surtax for high earners
- **Multiple Job Support**: Handle both salaried and hourly positions
- **Flexible Pay Periods**: Annual, monthly, semi-monthly, bi-weekly, and weekly
- **Tax Deductions**: Standard and itemized deductions
- **Tax Credits**: Both refundable and non-refundable credits
- **All Filing Statuses**: Single, Married Filing Jointly, Married Filing Separately, Head of Household
- **Real-time Updates**: Web interface updates calculations instantly

## 2025 Tax Information

This calculator uses the official 2025 tax brackets and standard deduction amounts:

### Standard Deductions (2025)
- Single: $15,000
- Married Filing Jointly: $30,000
- Married Filing Separately: $15,000
- Head of Household: $22,500

### FICA Tax Rates
- Social Security: 6.2% (on income up to $176,100)
- Medicare: 1.45% (on all income)
- Additional Medicare Tax: 0.9% (on income over threshold)

## Installation

### Prerequisites
- Python 3.7+
- FastAPI
- Uvicorn (for web interface)

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd tax-calculator
```

2. Install dependencies:
```bash
pip install fastapi uvicorn
```

## Usage

### Web Interface (Recommended)

1. Start the web server:
```bash
uvicorn app:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Use the intuitive web interface to:
   - Set your filing status
   - Add jobs (salaried or hourly)
   - Add deductions and tax credits
   - Calculate your tax burden

### Command Line Interface

Run the command-line version:
```bash
python main.py
```

Follow the interactive menu to input your tax information and calculate your burden.

## File Structure

```
├── app.py              # FastAPI web server
├── main.py             # Core tax calculation logic and CLI
├── index.html          # Web interface HTML
├── styles.css          # Web interface styling
├── script.js           # Web interface JavaScript
└── README.md           # This file
```

## API Endpoints

The web interface communicates with a REST API. Key endpoints include:

- `GET /` - Serve web interface
- `POST /add_job` - Add a new job
- `POST /set_status` - Set filing status
- `POST /add_deduct` - Add tax deduction
- `POST /add_rcredit` - Add refundable credit
- `POST /add_nrcredit` - Add non-refundable credit
- `GET /calculate` - Calculate total tax burden

## Tax Calculation Details

### Income Calculation
- Supports multiple jobs with different pay structures
- Handles various pay periods (weekly, bi-weekly, semi-monthly, monthly, annual)
- Calculates gross annual income from all sources

### Deduction Processing
- Automatic standard deduction based on filing status
- Support for itemized deductions
- Reduces taxable income dollar-for-dollar

### Tax Credit Application
- **Non-refundable credits**: Reduce tax liability to zero (but not below)
- **Refundable credits**: Can result in refunds even if no tax is owed

### FICA Tax Calculation
- Social Security tax with wage base limit
- Medicare tax on all income
- Additional Medicare tax for high earners with different thresholds by filing status

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines
- Follow existing code style
- Test both CLI and web interfaces
- Update documentation for new features
- Ensure tax calculations remain accurate

## Disclaimer

**Important**: This calculator is for educational and estimation purposes only. It should not be used as a substitute for professional tax advice. Tax laws are complex and subject to change. Always consult with a qualified tax professional or use official IRS resources for actual tax preparation.

The calculator uses simplified assumptions and may not account for all possible tax situations, deductions, or credits available under current tax law.

## License

This project is open source and available under the MIT License.
