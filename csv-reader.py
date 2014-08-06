import sys
import csv

#settings
source_file = 'data.csv'
filter_set = {'name':'John'}
labeled_row = {}
schema = []

def open_file(source_file):
    #open csv filestream
    csvfile = open(source_file,'r')
    #create csv reader object
    csvreader = csv.reader(csvfile, delimiter=',')
    return csvreader

def parse_operator(filter):
    #take the last character of the filter string and return it as the operator
    return filter[-1:]

#taken from http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def apply_filters(filters,row, schema):
    #iterate over all fields in the filter list
    for field_name in filters.keys():
        #default to a "Do not print" flag unless the filter passes
        print_row = False
        #only bother with filters that are in the schema
        if field_name in schema:
            #if the field contains numbers, apply number filter logic
            if is_number(row[field_name]):
                try:
                    operator = filters[field_name][-1:]
                    
                    #if there is no operator, or the equals sign is used, look for exact value
                    if is_number(operator) or operator == '=':
                        if float(row[field_name]) == float(filters[field_name][:-1]):
                            #set print flag to true and continue in the loop
                            print_row = True
                            continue
                        else:
                            #abandon the loop - the filter failed
                            break

                    #if the operator is less than or minus, look for values less than the value
                    elif operator == "<" or operator == "-":
                        if float(row[field_name]) <= float(filters[field_name][:-1]):
                            #set print flag to true and continue in the loop
                            print_row = True
                            continue
                        else:
                            #abandon the loop - the filter failed
                            break

                    #if the operator is greater than or plus, look for values more than the value
                    elif operator == ">" or operator == "+":
                        if float(row[field_name]) >= float(filters[field_name][:-1]):
                            #set print flag to true and continue in the loop
                            print_row = True
                            continue
                        else:
                            #abandon the loop - the filter failed
                            break
                #I believe this is actually unnecessary and a throwback to an alternate algorithm I was using
                except KeyError:
                    continue
            #if the row does not contain a number
            else:
                try:
                    #check for an exact match
                    if row[field_name] == filters[field_name]:
                        #set the print flag to true
                        print_row = True
                        continue
                    else:
                        #abandon the loop
                        break
                except KeyError:
                    continue
    #if, at the end of the loop, the print flag is set to "True", print the row
    if print_row:
        print row
        

def create_schema(data):
    #take the first item in the csv file and return it as the schema
    return data.next()

#combine the row with the schema so that for each row being evaluated the values and headers correspond
def apply_schema(schema,row):
    #empty dictionary
    labeled_row = {}
    #start from element 0
    index = 0
    for field in schema:
        #set the dict value of the name of the field to the value of the row
        labeled_row[field] = row[index]
        #increment the counter
        index+=1
    #after it's all over, return the finished dictionary
    return labeled_row


data = open_file(source_file)
schema = create_schema(data)

for row in data:
    #generate the header/row data dictionary
    labeled_row = apply_schema(schema,row)
    #evaluate the row based on the filter and print if appropriate
    apply_filters(filter_set,labeled_row, schema)