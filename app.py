from flask import Flask, render_template,request
import pickle
from xgboost import Booster
def prediction(arrayofinputs):
    try:
        booster = Booster()
        booster.load_model(r'test_model.bin')
        with open(r'xgboost_native_model_from_test_model.pkl-0.bin' , 'rb') as file:
            model = pickle.load(file)
    except FileNotFoundError:
        return  

    ans=model.predict(arrayofinputs)
    return ans

app = Flask(__name__)

@app.route('/')  # url binding
def loadhome():
    return render_template('Home.html')


@app.route('/form')
def dataform():
    return render_template('DATA_ENTRY.html',res = None)


@app.route('/submit', methods=['POST'])  # url binding
def user():
    Education = request.form['Education']
    ApplicantIncome = request.form['ApplicantIncome']
    Coapplicant = request.form['CoapplicantIncome']
    LoanAmount = request.form['LoanAmount']
    LoanAmountTerm = request.form['Loan_Amount_Term']
    CreditHistory = request.form['Credit_History']
    dependents = request.form['Dependents']
    property = request.form['Property_Area']
    gender = request.form['Gender']
    married=request.form['Married']
    self_employed=request.form['Self_Employed']
    if Education == 'Graduate':
        se1,se2 = 1,0
    else:
        se1,se2 = 0,1
    if dependents == '0':
        s3, s0, s1, s2 = 0, 1, 0, 0
    elif dependents == '1':
        s3, s0, s1, s2 = 0, 0, 1, 0
    elif dependents == '2':
        s3, s0, s1, s2 = 0, 0, 0, 1
    elif dependents == '3+':
        s3, s0, s1, s2 = 1, 0, 0, 0
    if property == 'Rural':
        sp1, sp2, sp3 = 1, 0, 0
    elif property == 'Semi-urban':
        sp1, sp2, sp3 = 0, 1, 0
    elif property == 'Urban':
        sp1, sp2, sp3 = 0, 0, 1
    if gender == 'Female':
        sg1,sg2=1,0
    elif gender=='Male':
        sg1,sg2=0,1
    if married=='Yes':
        sm1,sm2=0,1
    else:
        sm1,sm2=1,0
    if self_employed == 'Yes':
        semp1,semp2=0,1
    else:
        semp1,semp2=1,0
    # Education, Applicant Income, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, dependents(4), property(3)

    arrayofinputs = [[float(ApplicantIncome), float(Coapplicant), float(
        LoanAmount), float(LoanAmountTerm), float(CreditHistory), float(sg1), float(sg2),float(sm1),float(sm2), float(s3), float(s0), float(s1), float(s2), float(se1), float(se2), 
        float(semp1),float(semp2),float(sp1),float(sp2),float(sp3)]]
    
    ans=prediction(arrayofinputs)
    if  ans == 0:
        result='Rejected'
    else:
        result='Approved'
    result = str(result)
    print(result)
    return render_template('DATA_ENTRY.html',res = result)

if __name__ == '__main__':
   app.run()