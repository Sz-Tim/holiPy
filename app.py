import csv
from flask import Flask, render_template, request
from functools import reduce
import io
import operator
import os
import pandas
import random
import smtplib
import tablib

def randomizer():
    dataframe = pandas.read_csv('data/user_orig.csv')
    recip = list(dataframe['giver'])
    cp = pandas.Series(list(dataframe['couple']), dataframe['giver'])
    giv_ls = list(cp[dataframe['giver']])
    rec_ls = list(cp[recip])
    
    while([i for i, j in zip(giv_ls, rec_ls) if i == j]):
        random.shuffle(recip)
        rec_ls = list(cp[recip])

    dataframe['recipient'] = recip
    print(dataframe)

    dataframe.to_csv('data/user_new.csv', index=False)
    
def send_email(og_name, og_email, sbjct, gift_lim, dataframe):
    
    nPs = [0]*len(dataframe)
    for i in range(0, len(nPs)):
        nPs[i] = sum(dataframe['couple'] != dataframe['couple'][i])
    nPs_pr = [(1 - 1/x) for x in nPs]
    tPr = round((1-reduce(operator.mul, nPs_pr,1))*100, 0)
    body = '''Hi %s,\n\n
    
    This year, you have been randomly assigned to give a gift to %s.\n\n
    The pairings were generated and sent automatically, so apologies if you are giving \
    a gift to the same person as last year. Since there are only %s possibilities for \
    you, there is actually a %s%% chance of that happening each year, and a %s%% chance \
    of that happening to at least one person.\n\n
    Please keep in mind that the gift limit is $%s. If you have any questions, \
    contact %s at %s.'''
    
    for i in range(0,len(dataframe)):
        body_i = body % (dataframe['giver'][i], dataframe['recipient'][i], nPs[i],
                         round(1/nPs[i]*100, 0), tPr, gift_lim, 
                         og_name, og_email)
        email_text = 'Subject: {}\n\n{}'.format(sbjct, body_i)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login("HolidayGiftR@gmail.com", "holipygiftr")
        server.sendmail("HolidayGiftR@gmail.com", dataframe['email'][i], email_text)
        server.close()
    


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
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
            sbjct = request.form['sbjct']
            gift_lim = request.form['gift_lim']
            send_email(email_nm, email_eml, sbjct, gift_lim, dataframe)
            return render_template('emails_sent.html', og_nm=email_nm,\
                                   nPart=dataframe.shape[0])


if __name__ == '__main__':
    app.run()