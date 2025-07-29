// Tax Calculator Web UI - API-driven
class TaxCalculator {
    constructor() {
        this.filingStatus = null;
        this.jobs = [];
        this.deductions = [];
        this.refundableCredits = [];
        this.nonRefundableCredits = [];
        this.standardDeductionAdded = false;
        
        this.initializeEventListeners();
        this.loadStateFromAPI();
    }

    // API helper methods
    async apiCall(endpoint, method = 'GET', params = {}) {
        try {
            let url = endpoint;
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };
            
            if (method === 'GET' && Object.keys(params).length > 0) {
                const queryString = new URLSearchParams(params).toString();
                url += '?' + queryString;
            } else if (method === 'POST' && Object.keys(params).length > 0) {
                options.body = JSON.stringify(params);
            }
            
            const response = await fetch(url, options);
            
            if (!response.ok) {
                throw new Error(`API call failed: ${response.status}`);
            }
            
            const result = await response.json();
            
            // Check if the result has a success field and it's false
            if (result && result.hasOwnProperty('success') && !result.success) {
                throw new Error('Operation failed');
            }
            
            return result;
        } catch (error) {
            console.error('API call error:', error);
            throw error;
        }
    }

    // Load current state from API
    async loadStateFromAPI() {
        try {
            // Load filing status
            const statusResult = await this.apiCall('/get_filing_status');
            this.filingStatus = statusResult.status;
            
            // Load jobs
            const jobsResult = await this.apiCall('/get_jobs');
            this.jobs = jobsResult.jobs;
            
            // Load deductions
            const deductionsResult = await this.apiCall('/get_deductions');
            this.deductions = deductionsResult.deductions;
            
            // Load refundable credits
            const rcreditsResult = await this.apiCall('/get_refundable_credits');
            this.refundableCredits = rcreditsResult.refundable_credits;
            
            // Load non-refundable credits
            const nrcreditsResult = await this.apiCall('/get_non_refundable_credits');
            this.nonRefundableCredits = nrcreditsResult.non_refundable_credits;
            
            // Load standard deduction status
            const standardResult = await this.apiCall('/get_standard_deduction_added');
            this.standardDeductionAdded = standardResult.standard_deduction_added;
            
            this.updateDisplay();
        } catch (error) {
            console.error('Failed to load state from API:', error);
        }
    }

    // Set filing status
    async setFilingStatus(status) {
        try {
            await this.apiCall('/set_status', 'POST', { status });
            this.filingStatus = status;
            this.updateDisplay();
        } catch (error) {
            this.showMessage('Failed to set filing status: ' + error.message, 'error');
        }
    }

    // Add job
    async addJob(description, salary, amount, period, hours = 0) {
        try {
            // Get period multiplier from API
            const periodResult = await this.apiCall('/get_period_multiplier', 'GET', { period });
            const periods = periodResult.multiplier;
            
            if (periods === -1) {
                throw new Error('Invalid period.');
            }
            
            const result = await this.apiCall('/add_job', 'POST', {
                desc: description,
                salary: salary ? 1 : 0,
                amount: parseFloat(amount),
                periods: periods,
                hours: parseFloat(hours)
            });
            
            if (result.success) {
                // Reload jobs from API
                const jobsResult = await this.apiCall('/get_jobs');
                this.jobs = jobsResult.jobs;
                this.updateDisplay();
            }
        } catch (error) {
            throw new Error('Failed to add job: ' + error.message);
        }
    }

    // Remove job
    async removeJob(index) {
        try {
            await this.apiCall('/remove_job', 'POST', { index });
            
            // Reload jobs from API
            const jobsResult = await this.apiCall('/get_jobs');
            this.jobs = jobsResult.jobs;
            this.updateDisplay();
        } catch (error) {
            this.showMessage('Failed to remove job: ' + error.message, 'error');
        }
    }

    // Add deduction
    async addDeduction(description, amount) {
        try {
            await this.apiCall('/add_deduct', 'POST', {
                desc: description,
                amount: parseFloat(amount)
            });
            
            // Reload deductions from API
            const deductionsResult = await this.apiCall('/get_deductions');
            this.deductions = deductionsResult.deductions;
            
            // Check if this is the standard deduction
            if (description.toLowerCase().includes('standard') || 
                [15000, 22500, 30000].includes(parseFloat(amount))) {
                this.standardDeductionAdded = true;
            }
            
            this.updateDisplay();
        } catch (error) {
            throw new Error('Failed to add deduction: ' + error.message);
        }
    }

    // Remove deduction
    async removeDeduction(index) {
        try {
            await this.apiCall('/remove_deduct', 'POST', { index });
            
            // Reload deductions from API
            const deductionsResult = await this.apiCall('/get_deductions');
            this.deductions = deductionsResult.deductions;
            this.updateDisplay();
        } catch (error) {
            this.showMessage('Failed to remove deduction: ' + error.message, 'error');
        }
    }

    // Add refundable credit
    async addRefundableCredit(description, amount) {
        try {
            await this.apiCall('/add_rcredit', 'POST', {
                desc: description,
                amount: parseFloat(amount)
            });
            
            // Reload refundable credits from API
            const rcreditsResult = await this.apiCall('/get_refundable_credits');
            this.refundableCredits = rcreditsResult.refundable_credits;
            this.updateDisplay();
        } catch (error) {
            throw new Error('Failed to add refundable credit: ' + error.message);
        }
    }

    // Remove refundable credit
    async removeRefundableCredit(index) {
        try {
            await this.apiCall('/remove_rcredit', 'POST', { index });
            
            // Reload refundable credits from API
            const rcreditsResult = await this.apiCall('/get_refundable_credits');
            this.refundableCredits = rcreditsResult.refundable_credits;
            this.updateDisplay();
        } catch (error) {
            this.showMessage('Failed to remove refundable credit: ' + error.message, 'error');
        }
    }

    // Add non-refundable credit
    async addNonRefundableCredit(description, amount) {
        try {
            await this.apiCall('/add_nrcredit', 'POST', {
                desc: description,
                amount: parseFloat(amount)
            });
            
            // Reload non-refundable credits from API
            const nrcreditsResult = await this.apiCall('/get_non_refundable_credits');
            this.nonRefundableCredits = nrcreditsResult.non_refundable_credits;
            this.updateDisplay();
        } catch (error) {
            throw new Error('Failed to add non-refundable credit: ' + error.message);
        }
    }

    // Remove non-refundable credit
    async removeNonRefundableCredit(index) {
        try {
            await this.apiCall('/remove_nrcredit', 'POST', { index });
            
            // Reload non-refundable credits from API
            const nrcreditsResult = await this.apiCall('/get_non_refundable_credits');
            this.nonRefundableCredits = nrcreditsResult.non_refundable_credits;
            this.updateDisplay();
        } catch (error) {
            this.showMessage('Failed to remove non-refundable credit: ' + error.message, 'error');
        }
    }

    // Calculate total tax burden using API
    async calculate() {
        try {
            const result = await this.apiCall('/calculate', 'GET');
            return result;
        } catch (error) {
            throw new Error('Failed to calculate taxes: ' + error.message);
        }
    }

    // Get standard deduction amount from API
    async getStandardDeductionAmount() {
        try {
            const result = await this.apiCall('/get_standard_deduction_amount', 'GET');
            return result.amount;
        } catch (error) {
            throw new Error('Failed to get standard deduction amount: ' + error.message);
        }
    }

    // Update display
    updateDisplay() {
        this.updateStatusDisplay();
        this.updateJobsDisplay();
        this.updateDeductionsDisplay();
        this.updateCreditsDisplay();
        this.updateStandardDeductionButton();
    }

    // Update status display
    async updateStatusDisplay() {
        try {
            const statusNamesResult = await this.apiCall('/get_status_names');
            const statusNames = statusNamesResult.status_names;
            
            document.getElementById('current-status').textContent = 
                this.filingStatus ? statusNames[this.filingStatus] : 'Not set';
            
            // Update button states
            document.querySelectorAll('.status-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.status === this.filingStatus) {
                    btn.classList.add('active');
                }
            });
        } catch (error) {
            console.error('Failed to update status display:', error);
        }
    }

    // Update jobs display
    updateJobsDisplay() {
        const container = document.getElementById('jobs-container');
        container.innerHTML = '';
        
        if (this.jobs.length === 0) {
            container.innerHTML = '<div class="empty-message">No jobs added yet.</div>';
            return;
        }
        
        this.jobs.forEach((job, index) => {
            const card = document.createElement('div');
            card.className = 'item-card';
            
            let details;
            if (job[1]) { // salary is true
                details = `$${job[2].toLocaleString('en-US', {minimumFractionDigits: 2})} (${job[3]} periods)`;
            } else {
                details = `$${job[2].toFixed(2)}/hour (${job[4]} hours, ${job[3]} periods)`;
            }
            
            card.innerHTML = `
                <div class="item-info">
                    <div class="item-description">${job[0]}</div>
                    <div class="item-details">${details}</div>
                </div>
                <button class="btn btn-danger" onclick="calculator.removeJob(${index})">Remove</button>
            `;
            
            container.appendChild(card);
        });
    }

    // Update deductions display
    updateDeductionsDisplay() {
        const container = document.getElementById('deductions-container');
        container.innerHTML = '';
        
        if (this.deductions.length === 0) {
            container.innerHTML = '<div class="empty-message">No deductions added yet.</div>';
            return;
        }
        
        this.deductions.forEach((deduction, index) => {
            const card = document.createElement('div');
            card.className = 'item-card';
            
            card.innerHTML = `
                <div class="item-info">
                    <div class="item-description">${deduction[0]}</div>
                    <div class="item-details">$${deduction[1].toLocaleString('en-US', {minimumFractionDigits: 2})}</div>
                </div>
                <button class="btn btn-danger" onclick="calculator.removeDeduction(${index})">Remove</button>
            `;
            
            container.appendChild(card);
        });
    }

    // Update credits display
    updateCreditsDisplay() {
        // Refundable credits
        const rContainer = document.getElementById('rcredits-container');
        rContainer.innerHTML = '';
        
        if (this.refundableCredits.length === 0) {
            rContainer.innerHTML = '<div class="empty-message">No refundable credits added yet.</div>';
        } else {
            this.refundableCredits.forEach((credit, index) => {
                const card = document.createElement('div');
                card.className = 'item-card';
                
                card.innerHTML = `
                    <div class="item-info">
                        <div class="item-description">${credit[0]}</div>
                        <div class="item-details">$${credit[1].toLocaleString('en-US', {minimumFractionDigits: 2})}</div>
                    </div>
                    <button class="btn btn-danger" onclick="calculator.removeRefundableCredit(${index})">Remove</button>
                `;
                
                rContainer.appendChild(card);
            });
        }
        
        // Non-refundable credits
        const nrContainer = document.getElementById('nrcredits-container');
        nrContainer.innerHTML = '';
        
        if (this.nonRefundableCredits.length === 0) {
            nrContainer.innerHTML = '<div class="empty-message">No non-refundable credits added yet.</div>';
        } else {
            this.nonRefundableCredits.forEach((credit, index) => {
                const card = document.createElement('div');
                card.className = 'item-card';
                
                card.innerHTML = `
                    <div class="item-info">
                        <div class="item-description">${credit[0]}</div>
                        <div class="item-details">$${credit[1].toLocaleString('en-US', {minimumFractionDigits: 2})}</div>
                    </div>
                    <button class="btn btn-danger" onclick="calculator.removeNonRefundableCredit(${index})">Remove</button>
                `;
                
                nrContainer.appendChild(card);
            });
        }
    }

    // Update standard deduction button visibility
    updateStandardDeductionButton() {
        const standardBtn = document.getElementById('add-standard-deduction-btn');
        
        // Show button only if filing status is set and standard deduction is not added
        if (this.filingStatus && !this.standardDeductionAdded) {
            standardBtn.style.display = 'inline-block';
        } else {
            standardBtn.style.display = 'none';
        }
    }

    // Show results
    showResults(results) {
        document.getElementById('gross-income').textContent = `$${results.gross_income.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('taxable-income').textContent = `$${results.taxable_income.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('fica-tax').textContent = `$${results.fica_tax.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('income-tax').textContent = `$${results.income_tax.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('refundable-credits').textContent = `$${results.refundable_credits.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('total-tax').textContent = `$${results.total_tax.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        
        document.getElementById('results-section').style.display = 'block';
        document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
    }

    // Initialize event listeners
    initializeEventListeners() {
        // Filing status buttons
        document.querySelectorAll('.status-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.setFilingStatus(btn.dataset.status);
            });
        });

        // Job type change
        document.getElementById('job-type').addEventListener('change', (e) => {
            const hoursRow = document.getElementById('hours-row');
            if (e.target.value === 'hourly') {
                hoursRow.style.display = 'flex';
            } else {
                hoursRow.style.display = 'none';
            }
        });

        // Add job button
        document.getElementById('add-job-btn').addEventListener('click', async () => {
            const description = document.getElementById('job-description').value.trim();
            const jobType = document.getElementById('job-type').value;
            const amount = document.getElementById('job-amount').value;
            const period = document.getElementById('job-period').value;
            const hours = document.getElementById('job-hours').value;

            if (!description || !amount) {
                this.showMessage('Please fill in all required fields.', 'error');
                return;
            }

            try {
                if (jobType === 'salary') {
                    await this.addJob(description, true, amount, period);
                } else {
                    if (!hours) {
                        this.showMessage('Please enter hours worked for hourly jobs.', 'error');
                        return;
                    }
                    await this.addJob(description, false, amount, period, hours);
                }
                
                this.clearJobForm();
                this.showMessage('Job added successfully!', 'success');
            } catch (error) {
                this.showMessage(error.message, 'error');
            }
        });

        // Add deduction button
        document.getElementById('add-deduction-btn').addEventListener('click', async () => {
            const description = document.getElementById('deduction-description').value.trim();
            const amount = document.getElementById('deduction-amount').value;

            if (!description || !amount) {
                this.showMessage('Please fill in all required fields.', 'error');
                return;
            }

            try {
                await this.addDeduction(description, amount);
                this.clearDeductionForm();
                this.showMessage('Deduction added successfully!', 'success');
            } catch (error) {
                this.showMessage(error.message, 'error');
            }
        });

        // Add standard deduction button
        document.getElementById('add-standard-deduction-btn').addEventListener('click', async () => {
            try {
                const amount = await this.getStandardDeductionAmount();
                await this.addDeduction('Standard Deduction', amount);
                this.showMessage(`Standard deduction of $${amount.toLocaleString('en-US', {minimumFractionDigits: 2})} added successfully!`, 'success');
            } catch (error) {
                this.showMessage(error.message, 'error');
            }
        });

        // Add refundable credit button
        document.getElementById('add-rcredit-btn').addEventListener('click', async () => {
            const description = document.getElementById('rcredit-description').value.trim();
            const amount = document.getElementById('rcredit-amount').value;

            if (!description || !amount) {
                this.showMessage('Please fill in all required fields.', 'error');
                return;
            }

            try {
                await this.addRefundableCredit(description, amount);
                this.clearCreditForm('rcredit');
                this.showMessage('Refundable credit added successfully!', 'success');
            } catch (error) {
                this.showMessage(error.message, 'error');
            }
        });

        // Add non-refundable credit button
        document.getElementById('add-nrcredit-btn').addEventListener('click', async () => {
            const description = document.getElementById('nrcredit-description').value.trim();
            const amount = document.getElementById('nrcredit-amount').value;

            if (!description || !amount) {
                this.showMessage('Please fill in all required fields.', 'error');
                return;
            }

            try {
                await this.addNonRefundableCredit(description, amount);
                this.clearCreditForm('nrcredit');
                this.showMessage('Non-refundable credit added successfully!', 'success');
            } catch (error) {
                this.showMessage(error.message, 'error');
            }
        });

        // Calculate button
        document.getElementById('calculate-btn').addEventListener('click', async () => {
            try {
                const results = await this.calculate();
                this.showResults(results);
                this.showMessage('Tax calculation completed successfully!', 'success');
            } catch (error) {
                this.showMessage(error.message, 'error');
            }
        });
    }

    // Clear forms
    clearJobForm() {
        document.getElementById('job-description').value = '';
        document.getElementById('job-amount').value = '';
        document.getElementById('job-hours').value = '';
        document.getElementById('job-type').value = 'salary';
        document.getElementById('hours-row').style.display = 'none';
    }

    clearDeductionForm() {
        document.getElementById('deduction-description').value = '';
        document.getElementById('deduction-amount').value = '';
    }

    clearCreditForm(type) {
        document.getElementById(`${type}-description`).value = '';
        document.getElementById(`${type}-amount`).value = '';
    }

    // Show message
    showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        document.querySelector('.main-content').insertBefore(messageDiv, document.querySelector('.section'));
        
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}

// Initialize the calculator when the page loads
let calculator;
document.addEventListener('DOMContentLoaded', () => {
    calculator = new TaxCalculator();
});
