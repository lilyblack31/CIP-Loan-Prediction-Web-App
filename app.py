# save this as app.py
from flask import Flask, escape, request, render_template
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/novelty')
def novelty():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        name = request.form['name']
        loan_id = request.form['loan_id']
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        self_employed = request.form['self_employed']
        property_area = request.form['property_area']
        credit_history = float(request.form['credit_history'])
        loan_amount = float(request.form['loan_amount'])
        loan_term = float(request.form['loan_term'])
        income = float(request.form['income'])
        co_income = float(request.form['co_income'])
        email_id = request.form['email_id']

        #gender
        if(gender == 'male'):
            male = 1
        else:
            male = 0
        
        #married status
        if(married == 'yes'):
            married_yes = 1
        else:
            married_yes = 0
        
        #dependents
        if(dependents == '1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif(dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif(dependents == '3+'):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0
        
        #education
        if(education == 'not_graduated'):
            not_grad = 1
        else:
            not_grad = 0
        
        #self employed
        if(self_employed == 'yes'):
            self_employed_yes = 1
        else:
            self_employed_yes = 0
        
        #property area
        if(property_area == 'semiurban'):
            semiurban = 1
            urban = 0
        elif(property_area == 'urban'):
            semiurban = 0
            urban = 1
        else:
            semiurban = 0
            urban = 0
        
        ApplicantIncomeLog = np.log(income)
        TotalIncomeLog = np.log(income + co_income)
        LoanAmountLog = np.log(loan_amount)
        LoanAmountTermLog = np.log(loan_term)

        prediction = model.predict([[credit_history, ApplicantIncomeLog, LoanAmountLog, LoanAmountTermLog, TotalIncomeLog, male, married_yes, dependents_1, dependents_2, dependents_3, not_grad, self_employed_yes, semiurban, urban ]])

        #print(prediction)

        if(prediction == "N"):
            prediction = "Not approved"
        else:
            prediction = "Approved"

        return render_template("prediction.html", prediction_text = "Loan Status for the user {} ({}) with Loan ID {} is {}".format(name, email_id, loan_id, prediction))

    else:
        return render_template("prediction.html")

if __name__ == "__main__":
    app.run(debug=True)