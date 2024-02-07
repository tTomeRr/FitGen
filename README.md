## FLEX - custom workout generator

FLEX

A Flask based application designed to generate customized workout plans for users based on their specified parameters.
If no existing workout aligns with the user's preferences, the application can create a workout plan using the OpenAI API.



## Project Architcture


## Screenshots


## Installation and Setup Instructions

1. Ensure you have Docker and Docker Compose installed on your system. 

2. Clone this repository.
   
  `git clone https://github.com/tTomeRr/Flex.git`

3. Navigate to the repository on your computer

4. Create .env file

  `touch app/.env`
  ```
  echo "POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_HOST=localhost
  POSTGRES_DB=flex
  GMAIL_USERNAME= # optional for sending mails
  GMAIL_PASSWORD= # optional for sending mails
  OPENAI_API_KEY= # optional for generating workouts using openai API
  APP_SECRET_KEY=key" > app/.env
```


5. Run the following command to start the application:

`docker-compose up`  

6. Visit the App:

`localhost:5000`

## Reflection

This was my final project for my DevOps bootcamp. The main goal of the project was to create a Flask application with full CI/CD DevOps tools, utilizing the technologies we had learned so far.
After months of study, watching hundreds of lectures, and going through thousands of notes, this was my first real experience applying all the DevOps tools we've been taught.
During the process of completing the project, I encountered lot of problems and bugs. It was challenging, but overcoming these obstacles and progressing step by step towards completion was rewarding.
Although the project may not be the best in terms of performance and efficiency, I'm proud of myself for finishing it, I learned a lot,
and I'm looking forward to working on more projects and expanding my knowledge with additional tools as I continue my DevOps journey.
