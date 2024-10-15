# Prompt Flows for User-Agent Interaction on Education Data
This project explicit a simple question-answering flow for teachers interact with an educational database about his students activities and exams in various disciplines, using AWS solutions like Bedrock, Lambda and Athena.

The flow was created in the AWS GenAI Accelerator Event and is inspired in the following project: https://github.com/aws-samples/alexa-and-bedrock-integration

The project architecture consists in a LLM that will receive a natural language question, convert it to a SQL query, execute the query in Athena, return the results to an AI Agent that will respond according to the context, guardrails and knowledge base provided.
![image](https://github.com/user-attachments/assets/c22aa887-3b1d-4443-b781-d1069ce7355b)

For querying the data, a table was created in AWS Athena with the following structure:

```
/*
Table: sampledb.genai_students_data

Description:
This table stores information about student activities, scores, and completion statuses across various chapters and lessons.
*/

Columns:

1. `instrument_group` (VARCHAR)
   - Description: Represents the name of the activity category or group.
   - Example: 'Quiz', 'Exam', 'Simulate', 'Test 1'

2. `score_ratio` (DOUBLE)
   - Description: Indicates the student's score for the activity, represented as a ratio.
   - Example: 0.85 (85% score)

3. `chapter` (VARCHAR)
   - Description: Represents the chapter or section within a lesson.
   - Example: 'Chapter 3', 'Introduction to Algebra'

4. `discipline` (VARCHAR)
   - Description: The subject or field of study.
   - Example: 'Mathematics', 'Science', 'History'

5. `lesson` (VARCHAR)
   - Description: Refers to the specific theme or lesson within the chapter.
   - Example: 'Linear Equations', 'Photosynthesis'

6. `activity_finished_date` (DATE)
   - Description: The date when the activity was finished. If the activity is not completed, the value can be NULL.
   - Example: '2023-09-21' (YYYY-MM-DD format)

7. `student_id` (VARCHAR)
   - Description: Unique identifier for the student, typically used for tracking purposes.
   - Example: 'STU123456'

8. `classroom_name` (VARCHAR)
   - Description: The name of the classroom or group the student is associated with.
   - Example: 'Class A', 'Advanced Math Group'

9. `category` (VARCHAR)
   - Description: Indicates the type of activity:
     - 'ATV' for regular activities (assignments, quizzes, etc.)
     - 'AVL' for assessments or exams.
   - Example: 'ATV' (Regular activity), 'AVL' (Exam)

10. `completion` (BIGINT)
    - Description: A status marker for the completion of the activity:
      - 0: The activity has not been started.
      - 1: The activity is completed.
      - 2: The activity has been started but not finished.
    - Example: 1 (Activity finished), 0 (Not started), 2 (In progress)
```

Here's a detailed version of the Flow:
![image](https://github.com/user-attachments/assets/121ab1e2-b2ec-408a-b017-a07c15ebf52f)
