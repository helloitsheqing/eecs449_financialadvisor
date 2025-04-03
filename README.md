# EECS449 Financial Advisor
Github Repository for EECS449 Conversational AI Project: Financial Advisor Tool

By: Anneliese Ferguson, Benjamin Yee, Cindy Zhang, Fabian Ruiz, Herman Wu, Heqing (HQ) Wang, Julia Morville, Vedikas Sridharan


to start ollama functionality (root terminal):
    1. run `ollama pull deepseek-r1:1.5b`
    2. run `ollama serve`

to start the program:
    1. create 2 separate terminals
    2. run `cd backend` on one and `cd frontend` on another
    3. run `python3 app.py` on backend
    4. run `npm start` on frontend

database management (root terminal):
    - by running the program and loggin in or signing up, database is created by default
    - however, if you wish to manage/view the database here are the steps for it:
        - before doing anything, run `chmod +x database.sh`
        - reset db: `./database.sh reset`
        - populate db: `./database.sh populate`
            - this populates the database with an admin user:
                - username: admin
                - password: admin123
    