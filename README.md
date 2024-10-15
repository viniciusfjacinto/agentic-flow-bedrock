# Prompt Flows for User-Agent Interaction on Education Data
This project explicit a simple question-answering flow for teachers interact with an educational database about his students, using AWS solutions like Bedrock, Lambda and Athena.

The flow was created in the AWS GenAI Accelerator Event and is inspired in the following project: https://github.com/aws-samples/alexa-and-bedrock-integration

The project architecture consists in a LLM that will receive a natural language question, convert it to a SQL query, execute the query in Athena, return the results to an AI Agent that will respond according to the context, guardrails and knowledge base provided.
![image](https://github.com/user-attachments/assets/c22aa887-3b1d-4443-b781-d1069ce7355b)

For querying the data, a table was created in AWS Athena with the following structure:

Here's a detailed version of the Flow:
![image](https://github.com/user-attachments/assets/121ab1e2-b2ec-408a-b017-a07c15ebf52f)
