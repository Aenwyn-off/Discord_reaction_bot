<h1 align="center">DiscordAPI_Reactions_Bot </h1>

This discord bot was created as a practice to learn how to work with APIs, Docker and databases.

It uses the Pycord library (https://docs.pycord.dev/en/stable/) 

The bot implements:
- Add emotion to a user's message;
- Remove one emotion from a user;
- Remove all emotion from the user;

Bot link: https://discord.com/api/oauth2/authorize?client_id=1129455119143010416&permissions=8&scope=bot (Not deployed yet.)

#


### :computer: Technologies:
- Discord API (Pycord);
- Docker (Compose);
- DataBases (PostgreSQL, SQLAlchemy).
---





### :hammer_and_wrench: Installation:
1. $ pip install -r requirements.txt
2. Create **.env** file in your project directory and add the following variables to the **.env** environment, to work with the python_dotenv library:
  
       - BOT_TOKEN = <Api key from Discord Developer Portal>
       - URL = <URL of the PostgreSQL database>  

  **Optional**

3. You can set up a project from docker-compose by using the command "docker-compose up"