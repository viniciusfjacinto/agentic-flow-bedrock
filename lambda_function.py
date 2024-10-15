import json
import boto3
import os
import time
import re  # Import the regex module

# Initialize the Athena and S3 services
athena_client = boto3.client('athena', region_name=os.environ['region'])
s3_output = os.environ['output'] 
database = os.environ['database']

def execute_athena_query(query_string, database):
    # Execute the query
    response = athena_client.start_query_execution(
        QueryString=query_string,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': s3_output 
        }
    )
    
    # Get the QueryExecutionId to check the status of the query
    query_execution_id = response['QueryExecutionId']
    
    # Check the status of the query until it's done
    status = 'RUNNING'
    while status in ['RUNNING', 'QUEUED']:
        response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = response['QueryExecution']['Status']['State']
        if status == 'FAILED':
            raise Exception("Athena query failed: {}".format(response['QueryExecution']['Status']['StateChangeReason']))
        elif status == 'CANCELLED':
            raise Exception("Athena query was cancelled")
        time.sleep(1)  # Wait before checking the status again
    
    # Once the query is complete, return the QueryExecutionId to retrieve the results
    return query_execution_id

def get_query_results(query_execution_id):
    # Fetch the query results from Athena
    result = athena_client.get_query_results(QueryExecutionId=query_execution_id)
    
    # Parse and return the query result data
    rows = result['ResultSet']['Rows']
    
    # Extract column headers
    headers = [col['VarCharValue'] for col in rows[0]['Data']]
    
    # Extract data rows (ignoring the first row which is the header)
    data_rows = []
    for row in rows[1:]:
        data_row = [col.get('VarCharValue', '') for col in row['Data']]
        data_rows.append(data_row)
    
    return headers, data_rows

# Lambda handler function
def lambda_handler(event, context):
    try:
        # Extract the query and the question from the event using regex
        query_string = event['node']['inputs'][0]['value']
        
        # Use regex to extract the content between "sql``` ```" and "question``` ```"
        question_pattern = r'question```(.*?)```'
        query_pattern = r'sql```(.*?)```'
        
        # Search for the question and the SQL query using regex
        question_match = re.search(question_pattern, query_string, re.DOTALL)
        query_match = re.search(query_pattern, query_string, re.DOTALL)
        
        if not question_match or not query_match:
            raise Exception("Invalid input format. Could not find SQL or question.")
        
        # Get the question and SQL query from the matches
        user_question = question_match.group(1).strip()
        sql_query = query_match.group(1).strip()
        
        # Execute the Athena query
        query_execution_id = execute_athena_query(sql_query, database)
        
        # Retrieve the query results
        query_results = get_query_results(query_execution_id)
        
        # Format the output
        result_output = f"User question: {user_question} \nQuery results: {str(query_results[1])}"
        
        # Print the result for debugging
        print("Query executed:", sql_query)
        print("Query results:", query_results[1])
        print("User question:", user_question)
        
        return result_output
    
    except Exception as e:
        print("Error executing Athena query:", str(e))
        return str(e)
