import sys
import csv

source_file = 'data.csv'
filter_set = {}
schema = []

def open_file(source_file):
    csvfile = open(source_file,'r')
    csvreader = csv.reader(csvfile, delimiter=',')
    return csvreader

def apply_filter(filters,row):
    print 'lol'

def create_schema(data):
    return data.next()

data = open_file(source_file)
schema = create_schema(data)

for row in data:
    apply_filter(filter_set,row)