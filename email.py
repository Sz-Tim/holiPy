import smtplib
import pandas
from functools import reduce # Valid in Python 2.6+, required in Python 3
import operator

sender = "HolidayGiftR@gmail.com"
pswd = "holipygiftr"
contact_email = "Wallace.Szewczyk@gmail.com"
contact_name = "Wallace"

dataframe = pandas.read_csv('data/testList.csv')

sent_from = sender
subject = 'Secret Santa 2017'
body = '''Hi %s,\n\n
This year, you have been randomly assigned to give a gift to %s.\n\n
The pairings were generated and sent automatically, so apologies if you are giving 
a gift to the same person as last year. Since there are only %s possibilities for 
you, there is actually a %s%% chance of that happening each year, and a %s%% chance 
of that happening to at least one person.\n\n
Please keep in mind that the gift limit is $%s. If you have any questions, 
contact %s at %s.'''

nPs = [0]*len(dataframe)
for i in range(0, len(nPs)):
    nPs[i] = sum(dataframe['couple'] != dataframe['couple'][i])
nPs_pr = [(1 - 1/x) for x in nPs]
tPr = round((1-reduce(operator.mul, nPs_pr,1))*100, 0)
giftLim = 2000

for i in range(0,len(dataframe)):
    body_i = body % (dataframe['giver'][i], dataframe['recip'][i], nPs[i],
                     round(1/nPs[i]*100, 0), tPr, giftLim, 
                     contact_name, contact_email)
    email_text = 'Subject: {}\n\n{}'.format(subject, body_i)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(sender, pswd)
    server.sendmail(sent_from, dataframe['email'][i], email_text)
    server.close()


