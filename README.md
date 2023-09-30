Hi, the task output files are provided in two ways, both contains the code of ETL process and code used for data validation and its results. Second one is a containerized etl pipeline where data is also being ingested to postgres.
1. First as a .ipynb file (Honeypot_Task_Submission.ipynb) 
2. Second as a containerized etl pipeline containing .py and yaml scripts (you need to have docker installed for that and then just need to run docker-compose up command in the root directory of project.)

Summary of the approach:
- First focus was on getting rid of non-contributing non-numeric characters which I did by replacing all those characters by keyword named "splitter which was used for splitting the string into substrings.
- After having the list of substrings, it was important to get rid of further noise from each substring to convert them into numeric integer value. It was a bit easy to convert those substrings into integer value which don't contain too many dots or commas. If there are only one or two dots or comma, I converted the European format into US format, and the if digit is less than or equal to 3 characters, it needs to be multiplied with 1000 to have yearly based salary, and then numeric values are stored in list to compute mean of them at the end.
- Alternatively, there were some special cases of strings which contain only space or dot as non-numeric character, so they need to be splitted by these character to get list of substrings. Once I have substrings, then we can follow the same process as above, but for this dataset as we didn't have too many such cases so I simply get rid of the noise and converted them into integer value, and then similary as above computed the mean of numeric values to get average of salaries.

Salary_Parse function detailed overview:

The function aims to handle various salary string formats and convert them into a single integer value. It accommodate different formats, including spaces and special cases.

Here's a breakdown of what the function does:

1. It checks if the input string is a NaN value, If it's NaN, it returns None.

2. It replaces non-numeric characters (except for commas, periods, space, and the characters ´') with the string 'splitter'. This effectively splits the input string into a list of substrings, each potentially containing numeric information. The use of 'splitter' helps separate different numeric parts in the input.

3. It iterates through the list of substrings created in step 2 and processes each substring.

4. For each substring, it removes the leading and trailing white spaces, commas and dot, and performs the following checks:

condition: If the substring has at most two periods (dots), at most one comma, and a length of less than 10 characters, it processes it further.
. It removes any characters that are not digits, commas, or dots from the substring.
. It replaces dot with empty string and commas with dot to ensure a consistent decimal separator. (Conversion from European into US format)
. It handles a specific hard-coded salary value ('8085000') and converts it to '82500.0'. (did not handle it generically as this was the only value containing this unique format (80.85.000))
. If the resulting substring is not empty, it converts it to a numeric value and check if integer is not zero and length of it less than or equal to 3, if yes, then it needs to multiply with 1000 to have a yealy salary, otherwise appending as it is to the list named "list_parsed_values" (this list contains numeric integers converted from substrings {wether it would be parse from string in the form of range or without range})

5. If a substring doesn't match the step 4 condition, then it performs the following checks (this is for special cases where string doesn't get split by "splitter" as it doesn't contain any non-numeric character except dot and space)

. If a substring contains space, it is splitted by space and processes each resulting substring items by repacing all non-numeric characters with empty string, and adding numeric values to list "list_parsed_values" in case if they are not empty.
. If a substring doesn't contain space and contains more than two dots, it splits it into two parts around the second dot, and then repace all non-numeric characters with empty string, and add numeric values to "list_parsed_values" list.

6. After processing all substrings, if list named "list_parsed_values" is not empty, the function calculates the mean of th numeric values in "list_parsed_values" and returns it as an integer, else it returns None.