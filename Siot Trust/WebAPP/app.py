#importing required libraries

from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from flask import flash
from flask_material import Material
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score


app = Flask(__name__)
Material(app)
app.secret_key="dont tell any one"

@app.route('/')
def home():
    return render_template('login.html')
    # User is not loggedin redirect to login page


@app.route('/main')
def main():
    return render_template('index.html')
    # User is not loggedin redirect to login page


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/',methods=["POST"])
def login():
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pass']
        if username=='admin' and password=='admin':
            return render_template("index.html")
        else:
            flash("wrong password")
            return render_template("login.html")


@app.route('/main',methods=["POST"])
def analyze():
	if request.method == 'POST':
		time = request.form['time']
		Trustor = request.form['Trustor']
		Trustee = request.form['Trustee']
		pkf = request.form['pkf']
		pkd = request.form['pkd']
		pdr = request.form['pdr']
		frnd =request.form['frnd']
		coi = request.form['coi']
		did = request.form['did']
		dtype = request.form['dtype']
		dbrand = request.form['dbrand']
		dmodel = request.form['dmodel']
		drtype = request.form['drtype']
		drf = request.form['drf']
	

		sample_data = [time,Trustor,Trustee,pkf,pkd,pdr,frnd,coi,did,dtype,dbrand,dmodel,drtype,drf]
		clean_data = [float(i) for i in sample_data]
		ex1 = np.array(clean_data).reshape(1,-1)




		data=pd.read_csv("trust1.csv")
		data=data.replace(["Smartphone","Smartwatch","Smart Speaker","Smart Thermostat","Smart Bulb","Smart Lock","Smart TV","Smart Camera","Smart Refrigerator","Smart Plug"],[0,1,2,3,4,5,6,7,8,9])
		data=data.replace(["iPhone 12","Galaxy Watch","Echo Dot","Learning Thermostat","Hue White & Color Ambiance","Assure Lock SL","Bravia X900H","Pro 3","RF28R7351SG","Kasa Smart Plug"],[0,1,2,3,4,5,6,7,8,9])
		data=data.replace(["Home Automation","Personal","Entertainment","Security","Fridge"],[0,1,2,3,4])
		data=data.replace(["Samsung","Apple","Amazon","Nest","Philips","Yale","Sony","Arlo","TP-Link"],[0,1,2,3,4,5,6,7,8])

		
		features = data
		kmeans = KMeans(n_clusters=2, random_state=42)

		data['Label'] = kmeans.fit_predict(features)
		X=data.iloc[:,:-1]

		y=data.iloc[:,-1:]
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
		clf=SVC()
		clf.fit(X_train, y_train)

		result=clf.predict(ex1)
		if result==1:
			class1="Trust"
		else:
			class1="Un Trust "


		return render_template('contact.html',class1=class1)

if __name__ == "__main__":
    app.run(debug=True)