import pandas as pd
import re

def parse_salary(salary_str):

    """
    input: salary string in any format
    output: parsed average salary in form of integer
    """

    if pd.isna(salary_str):
        return None
    
    # Remove non-numeric characters except for commas, periods, space, and ´'
    salary_str = re.sub(r"[^\d´'., ]", 'splitter', salary_str)
    salary_items_list = salary_str.split('splitter')
    list_parsed_values = []
    for salary_item in salary_items_list:
        salary_item = salary_item.strip(" .,")
        if salary_item.count('.') <= 2 and salary_item.count(',') <= 1 and len(salary_item) < 10:
            salary_item = re.sub(r'[^\d.,]', '', salary_item)
            salary_item = salary_item.replace('.', '').replace(',', '.')
            if salary_item != '':
                salary_item = '82500.0' if salary_item == '8085000' else salary_item  # Hard corded this specifc record
                numeric_value = int(float(salary_item))
                if len(str(numeric_value)) <= 3 and numeric_value != 0:
                    list_parsed_values.append(numeric_value * 1000)
                else:
                    list_parsed_values.append(numeric_value)
                    
        else:
            if ' ' in salary_item:
                salary_item_list = salary_item.split(' ')
                for salary_item in salary_item_list:
                    salary_item = re.sub(r'[^\d]', '', salary_item)
                    if salary_item != '':
                        numeric_value = int(float(salary_item))
                        list_parsed_values.append(numeric_value)
                        
            elif salary_item.count('.') > 2:
                salary_item_list = salary_item.split('.', 2)
                salary_item_list = [salary_item_list[0] + '.' + salary_item_list[1], salary_item_list[2]]
                salary_item_list = [int(re.sub(r'[^\d]', '', special_salary_item)) for special_salary_item in salary_item_list]
                list_parsed_values.extend(salary_item_list)

            
    if list_parsed_values:
        mean_salaries = int(sum(list_parsed_values ) / len(list_parsed_values ))
    else:
        return None
    
    return mean_salaries