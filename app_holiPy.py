#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:26:18 2017

@author: fossegrimen
"""

from flask import Flask, render_template, request
import csv
import io
import pandas
import random
import tablib
import os

def randomizer():
    dataframe = pandas.read_csv('data/user_orig.csv')
    recip = list(dataframe['giver'])
    cp = pandas.Series(list(dataframe['couple']), dataframe['giver'])

    while(list(cp[dataframe['giver']]) == list(cp[recip])):
        random.shuffle(recip)
        dataframe['recip'] = recip

    dataframe.to_csv('data/user_new.csv', index=False)


app_holiPy = Flask(__name__)

@app_holiPy.route('/index_holiPy', methods=['GET','POST'])
def index_holiPy():
    if request.method == 'GET':
        return render_template('index.html')
    else:        
        f = request.files['user_csv']
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        print(csv_input)
        for row in csv_input:
            print(row)

        stream.seek(0)
        user_orig = stream.read()
        fwr = open('data/user_orig.csv', 'w')
        fwr.write(user_orig)
        fwr.close()
        randomizer()
        dataframe = pandas.read_csv('data/user_new.csv')
        
        email_opt = request.form['email-opt']
        if email_opt == 'No':
            dataset = tablib.Dataset()
            with open(os.path.join(os.path.dirname(__file__), 'data/user_new.csv')) as f:
                dataset.csv = f.read()
            return dataset.html
        else:
            email_nm = request.form['og-name']
            email_eml = request.form['og-email']
            f_e = open('data/user_email.txt', 'w')
            f_e.write('%s <%s>' % (email_nm, email_eml))
            f_e.close()
            return render_template('emails_sent.html', og_nm=email_nm,\
                                   nPart=dataframe.shape[0])


if __name__ == '__main__':
    app_holiPy.run(debug=True)