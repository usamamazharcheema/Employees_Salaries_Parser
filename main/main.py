from time import sleep
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError
from os import environ
import matplotlib.pyplot as plt
from parse_salary import parse_salary

if __name__ == '__main__':
    while True:
        try:
            psql_engine = create_engine(environ["POSTGRESQL_CS"], pool_pre_ping=True, pool_size=10)
            break
        except OperationalError:
            sleep(0.1)
    print('Connection to PostgresSQL successful.')

    df_interviews_salary = pd.read_csv("input_data/Code Challenge Data.csv")
    df_interviews_salary['salary_processed'] = df_interviews_salary['salary'].apply(parse_salary)
    df_interviews_salary = df_interviews_salary.fillna(0)
    
    ### Count the total number of records in the interviews_salary table.
    df_interviews_salary_total_records = df_interviews_salary.shape[0]
    print(f"Total number of records: {df_interviews_salary_total_records}")

    ### Calculate the average, median, and percentile 75 of the salary column
    df_interviews_salary['salary_processed'] = df_interviews_salary['salary_processed'].astype('int64')
    # Average (mean) salary
    average_salary = df_interviews_salary['salary_processed'].mean()
    # Median salary
    median_salary = df_interviews_salary['salary_processed'].median()

    # 75th percentile salary
    percentile_75_salary = df_interviews_salary['salary_processed'].quantile(0.75)

    print(f"Average Salary: {average_salary}")
    print(f"Median Salary: {median_salary}")
    print(f"75th Percentile Salary: {percentile_75_salary}")

    # Create a histogram of the salary distribution
    plt.hist(df_interviews_salary['salary_processed'], bins=11, color='skyblue', edgecolor='black')
    plt.xlabel('Salary')
    plt.ylabel('Frequency')
    plt.title('Salary Distribution')
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    plt.show()

    df_interviews_salary = df_interviews_salary[['id', 'salary_processed']]
    df_interviews_salary.head(n=0).to_sql(name = "Employees_Salaries", con=psql_engine, if_exists='replace', index=False)
    try:
        df_interviews_salary.to_sql(name = 'Employees_Salaries', con=psql_engine, if_exists='append', index=False)
    except (OperationalError, ProgrammingError) as e:
        print('Error occured while inserting data in PostgreSQL; {}'.format(e.args))
    print('Data inserted to PostgreSQL')


    