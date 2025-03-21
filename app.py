from flask import Flask, request, render_template

app = Flask(__name__)

def calculate_price(bank_tx, credit_card_tx, bank_accounts, credit_cards, business_locations,
                    service_selection, num_employees, additional_services, require_ind_tax,
                    total_ind_tax_returns):
    # Base Calculations
    bank_transactions_cost = 423 + ((bank_tx + credit_card_tx - 40) * 2.5)
    complexity = (1 if bank_accounts > 1 else 0) + (1 if credit_cards > 1 else 0) + (1 if business_locations > 1 else 0)
    
    # Accounting Estimate (without year-end processing)
    if "Accounting" in service_selection:
        accounting = bank_transactions_cost + complexity * 75
    else:
        accounting = 0

    # Payroll Estimate
    if "Accounting" in service_selection:
        payroll = 125 if num_employees <= 10 else num_employees * 12
    else:
        payroll = 0

    # Cashflow Management Estimate
    if "Cashflow Management/Bill Pay" in additional_services:
        cashflow = max((bank_transactions_cost + complexity * 75) * 1.5, 650)
    else:
        cashflow = 0

    # Profit First Estimate
    if "Profit First" in additional_services:
        profit_first = max(700, bank_transactions_cost + complexity * 75)
    else:
        profit_first = 0

    # Corporate Tax Estimate
    if "Tax" in additional_services:
        corp_tax = (bank_transactions_cost + complexity * 75) * (5 / 12)
    else:
        corp_tax = 0

    # Individual Tax Estimate
    if require_ind_tax == "Yes":
        ind_tax = 100 * total_ind_tax_returns
    else:
        ind_tax = 0

    # Monthly and Annual Totals
    monthly_total = accounting + payroll + cashflow + profit_first + corp_tax + ind_tax
    annual_total = monthly_total * 12

    return monthly_total, annual_total

@app.route('/', methods=['GET', 'POST'])
def index():
    monthly = annual = None
    if request.method == 'POST':
        # Retrieve values from the form. Convert inputs as needed.
        bank_tx = float(request.form.get('bank_tx', 0))
        credit_card_tx = float(request.form.get('credit_card_tx', 0))
        bank_accounts = int(request.form.get('bank_accounts', 0))
        credit_cards = int(request.form.get('credit_cards', 0))
        business_locations = int(request.form.get('business_locations', 0))
        service_selection = request.form.get('service_selection', '')
        num_employees = int(request.form.get('num_employees', 0))
        additional_services = request.form.get('additional_services', '')
        require_ind_tax = request.form.get('require_ind_tax', 'No')
        total_ind_tax_returns = int(request.form.get('total_ind_tax_returns', 0))

        monthly, annual = calculate_price(bank_tx, credit_card_tx, bank_accounts, credit_cards,
                                            business_locations, service_selection, num_employees,
                                            additional_services, require_ind_tax, total_ind_tax_returns)
    return render_template('index.html', monthly=monthly, annual=annual)

if __name__ == '__main__':
    app.run(debug=True)
