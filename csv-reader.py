import sys
import csv

source_file = 'data2.csv'
filter_set = {'unique_id':'10-', 'height_in_inches':'100+'}
labeled_row = {}
schema = []

def open_file(source_file):
    csvfile = open(source_file,'r')
    csvreader = csv.reader(csvfile, delimiter=',')
    return csvreader

def parse_operator(filter):
    return filter[-1:]

#taken from http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def apply_filters(filters,row, schema):
    for field_name in schema:

        if is_number(row[field_name]):
            
            try:
                #determine which operator is being used
                operator = filters[field_name][-1:]
               
                #if there is no operator, or the equals sign is used, look for exact value
                if is_number(operator) or operator == '=':
                    if float(row[field_name]) == float(filters[field_name][:-1]):
                        continue
                    else:
                        break
                
                #if the operator is less than or minus, look for values less than the value
                elif operator == "<" or operator == "-":
                    if float(row[field_name]) <= float(filters[field_name][:-1]):
                        continue
                    else:
                        break
                
                #if the operator is greater than or plus, look for values more than the value
                elif operator == ">" or operator == "+":
                    if float(row[field_name]) >= float(filters[field_name][:-1]):
                        continue
                    else:
                        break
            
            except KeyError:
                continue
            except ValueError:
                break
        else:
            try:
                if row[field_name] == filters[field_name]:
                    continue
                else:
                    break
            except KeyError:
                continue
        return row
        

def create_schema(data):
    return data.next()

def apply_schema(schema,row):
    labeled_row = {}
    index = 0
    for field in schema:
        labeled_row[field] = row[index]
        index+=1
    return labeled_row


data = open_file(source_file)
schema = create_schema(data)

for row in data:
    labeled_row = apply_schema(schema,row)
    value = apply_filters(filter_set,labeled_row, schema)
    if value != None:
        print value