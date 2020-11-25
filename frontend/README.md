# Building the web app
## 1. Installing Dependencies

  First, you will need to have `npm`, `yarn`, `pip` (this should already come with Python), and `virtualenv` installed.  
  To install the UI dependencies, navigate to the `frontend/ui` folder in your terminal and run `yarn install` in this directory.  
  Next, for the backend dependencies, navigate to the `frontend/service` folder and run these commands in your terminal:
    
        virtualenv -p Python3 .
        source bin/activate
        pip install -r requirements.txt

## 2. Running the UI

  To start hosting the UI on your local machine, go to `frontend/ui` and run
  
        npm run build
        serve -s build -l 3000
        
  Enter `localhost:3000` in your browser to view the web app.

## 3. Running the backend

  To start running the backend, go to `frontend/service` and run
  
        virtualenv -p Python3 .
        source bin/activate
        FLASK_APP=app.py flask run
        
  You can enter `127.0.0.1:5000` to view the backend service.

## References
This web app was built using the template detailed here: https://towardsdatascience.com/create-a-complete-machine-learning-web-application-using-react-and-flask-859340bddb33