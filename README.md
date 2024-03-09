## FLEX - custom workout generator

FLEX

A Flask based application designed to generate customized workout plans for users based on their specified parameters.
If no existing workout aligns with the user's preferences, the application can create a workout plan using the OpenAI API.



## Project Architcture

![flex-diagram](https://github.com/tTomeRr/Flex/assets/129614080/e4611cb6-6e7a-4cf7-9a84-ba58c62671d1)
![sql](https://github.com/tTomeRr/Flex/assets/129614080/2f0f7b01-69f1-4cc6-bdb9-0df4424966ce)


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

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any improvements or bug fixes.


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Screenshots
![Screenshot 1](https://github.com/tTomeRr/Flex/assets/129614080/ee9e5746-6ac4-4cad-9ea9-6ca602fd30f2)
![Screenshot 2](https://github.com/tTomeRr/Flex/assets/129614080/f591c817-3238-41f0-8728-65aa5b2ac304)
![Screenshot 3](https://github.com/tTomeRr/Flex/assets/129614080/9746f700-25a3-4308-8ee7-eccb3e7b90c1)
![Screenshot 4](https://github.com/tTomeRr/Flex/assets/129614080/8c066a39-a573-4ad8-b483-06fd37f76444)
![Screenshot 5](https://github.com/tTomeRr/Flex/assets/129614080/b53df931-bbd5-41ff-a08e-49c9253a9a0a)
![Screenshot 6](https://github.com/tTomeRr/Flex/assets/129614080/3965a814-62bb-45b8-977e-55d5423d211e)
