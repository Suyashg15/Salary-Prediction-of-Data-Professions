from flask import Flask,render_template,request,jsonify
from sklearn.preprocessing import OrdinalEncoder
import pickle
import numpy as np

app = Flask(__name__)

salary_pred = pickle.load(open('model\Salary_prediction_decision_tree.pkl','rb'))

# Sample categorical features
categorical_features_designation = ['Analyst', 'Senior Analyst', 'Associate', 'Senior Manager', 'Manager', 'Director']
categorical_features_unit = ['Finance', 'IT', 'Marketing', 'Operations', 'Web', 'Management']

# Initialize OrdinalEncoder
encoder = OrdinalEncoder()

# Fit and transform the encoder for each categorical feature
encoded_designation = encoder.fit_transform([[category] for category in categorical_features_designation])
encoded_unit = encoder.fit_transform([[category] for category in categorical_features_unit])

# Create dictionaries to store the mapping of category to encoded value
designation_mapping = {category: int(encoded_value) for category, encoded_value in zip(categorical_features_designation, encoded_designation.flatten())}
unit_mapping = {category: int(encoded_value) for category, encoded_value in zip(categorical_features_unit, encoded_unit.flatten())}


@app.route('/',methods = ['GET'])
def home():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def predict():
    
    Designation = request.form['Designation']
    Unit = request.form['Unit']
    leaves_used = float(request.form['Leaves_used'])
    leaves_rem = float(request.form['Leaves_rem'])
    Rating = float(request.form['Rating'])
    past_exp = float(request.form['past_exp'])
    
    for i,j in designation_mapping.items():
        if i==Designation:
            design = j
            break
    
    for i,j in unit_mapping.items():
        if i==Unit:
            unit = j
            break
    
    input = [[design,unit,leaves_used,leaves_rem,Rating,past_exp]]
    print(input)
    pred = salary_pred.predict(input)
    final_prediction = pred[0]
    return render_template('index.html',prediction = final_prediction)

    
if __name__=="__main__":
    app.run(port=3000,debug=True)