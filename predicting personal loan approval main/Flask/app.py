# save this as app.py
from flask import Flask, escape, request, render_template
App =Flask(__name__,template_folder='templates/')
import pickle
import numpy as np
App = Flask(__name__)
model = pickle.load(open( r'rdf.pkl', 'rb'))
@App.route('/',methods=['GET',])
def home():
    return render_template("index.html")
@App.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        Gender = request.form['gender']
        Married = request.form['married']
        Dependents = request.form['dependents']
        Education = request.form['education']
        Self_Employed = request.form['employed']
        Credit_History = float(request.form['credit'])
        Property_Area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # gender
        if (Gender == "Male"):
            male=1
        else:
            male=0
        
        # married
        if(Married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # dependents
        if(Dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            #dependents_3 = 0
        elif(Dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            #dependents_3 = 0
        elif(Dependents=="3+"):
            dependents_1 = 0
            dependents_2 = 0
            #dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0  

        # education
        if (Education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

        # employed
        if (Self_Employed == "Yes"):
            employed_yes=1
        else:
            employed_yes=0

        # property area

        if(Property_Area=="Semiurban"):
            semiurban=1
            urban=0
        elif(Property_Area=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0


        ApplicantIncome= np.log(ApplicantIncome)
       # totalincome = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmount = np.log(LoanAmount)
        Loan_Amount_Term = np.log(Loan_Amount_Term)

        #prediction = model.predict([[Credit_History, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Termlog, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes,semiurban, urban ]])
        prediction=model.predict([[Credit_History, ApplicantIncome,LoanAmount, Loan_Amount_Term,  male, married_yes, dependents_1, dependents_2, not_graduate, employed_yes,semiurban, urban ]])

        print(prediction)

        if(prediction=="N"):
            prediction="No"
        else:
            prediction="Yes"
        #prediction=model.predict([[Credit_History, ApplicantIncome,LoanAmount, Loan_Amount_Term,  male, married_yes, dependents_1, dependents_2, not_graduate, employed_yes,semiurban, urban ]])
        #print(prediction)
        #prediction=int(prediction)
        #print(type(prediction))
    #if (prediction == 0):
     #   return render_template("prediction.html",result="Loan will not be Approver")
    #else:
      #  return render_template("prediction.html",result="Loan will  be Approver")
        return render_template("prediction.html", prediction_text="loan status is {}".format(prediction))
    else:
        return render_template("prediction.html")
if __name__ == "__main__":
    App.run(host='0.0.0.0',port=80,debug=True)