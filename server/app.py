from flask import Flask, request, render_template,jsonify
import json
import os
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
import re

#La clé de l'API OpenAI
os.environ['OPENAI_API_KEY'] = "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"

#la connexion à la base de données
db = SQLDatabase.from_uri("mysql+pymysql://root:redaredaredareda@127.0.0.1/REDA")

#Configuration de l'API OpenAI avec langchain
llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
#initialisation de l'application
app = Flask(__name__, template_folder='templates')
items=[]

def extract_number_from_string(string):
    # Define the regular expression pattern to match a number
    pattern = r'\d+\.?\d*'  # Matches one or more digits, optionally followed by a decimal point and more digits

    # Use the re.findall() function to find all matches of the pattern in the string
    matches = re.findall(pattern, string)

    # Check if any matches were found
    if matches:
        # Return the first match as a float or int depending on the presence of a decimal point
        return float(matches[0]) if '.' in matches[0] else int(matches[0])

    # Return None if no number was found in the string
    return None
serialized_percentages=[]
pourcentages = []
error=""
@app.route('/')
def home():
    return render_template('index.html',pourcentages=[],error="")
@app.route('/',methods=['POST'])
def getvalue():
    global pourcentages
    sql=request.form['request']
    try:
        response = db_chain.run(sql)
        pourcentages.append(extract_number_from_string(response));
        serialized_percentages = json.dumps(pourcentages)
        return render_template('index.html',pourcentages=serialized_percentages)
    except :
        serialized_percentages = json.dumps(pourcentages)
        return render_template('index.html',pourcentages=serialized_percentages)


if __name__ == '__main__':
    app.run(debug=True)