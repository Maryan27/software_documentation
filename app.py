import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src'))
sys.path.append(os.path.join(BASE_DIR, 'src', 'dal'))
sys.path.append(os.path.join(BASE_DIR, 'src', 'bll'))

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, InsuranceProduct         
from data_access import CSVAndDBAccess         
from business_logic import InsuranceManager       

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

engine = create_engine("sqlite:///insurance.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

data_access = CSVAndDBAccess(session)
manager = InsuranceManager(data_access)

@app.route("/")
def index():
    products = manager.get_all_products()
    return render_template("index.html", products=products)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_product = InsuranceProduct(
            client_name=request.form['client_name'],
            client_email=request.form['client_email'],
            policy_number=request.form['policy_number'],
            insurance_type=request.form['insurance_type'],
            amount=float(request.form['amount']),
            company_name=request.form.get('company_name', '')
        )

        date_str = request.form.get('start_date')
        if date_str:
            new_product.start_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            new_product.start_date = None

        session.add(new_product)
        session.commit()
        return redirect(url_for('index'))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    product = session.query(InsuranceProduct).get(id)
    if request.method == "POST":
        product.client_name = request.form['client_name']
        product.client_email = request.form['client_email']
        product.policy_number = request.form['policy_number']
        product.insurance_type = request.form['insurance_type']
        product.amount = float(request.form['amount'])
        product.company_name = request.form.get('company_name', '')

        date_str = request.form.get('start_date')
        if date_str:
            product.start_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            product.start_date = None

        session.commit()
        return redirect(url_for('index'))
    return render_template("edit.html", product=product)

@app.route("/delete/<int:id>")
def delete(id):
    product = session.query(InsuranceProduct).get(id)
    session.delete(product)
    session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)