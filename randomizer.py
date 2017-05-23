#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 20:54:57 2017

@author: fossegrimen
"""

import pandas
import random

dataframe = pandas.read_csv('data/testList.csv')
recip = list(dataframe['giver'])
cp = pandas.Series(list(dataframe['couple']), dataframe['giver'])

while(list(cp[dataframe['giver']]) == list(cp[recip])):
    random.shuffle(recip)
dataframe['recip'] = recip

dataframe.to_csv('data/testList.csv', index=False)
