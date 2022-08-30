# manoti_crm
 
Manoti CRM is an open source, free software package for companies of any size, foundations or freelancers. It includes different features for enterprise resource planning (ERP) and customer relationship management (CRM) but also other features for different activities. Manoti CRM is written in Django language framework, with Python

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out for instructions on how to deploy this app to Heroku and also run it locally.

Alternatively, you can deploy it using this Heroku Button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)


Run the app locally
Before continuing, make sure the app’s dependencies have been installed locally.

The app is almost ready to start locally. Django uses local assets, so first, you’ll need to run collectstatic:

python manage.py collectstatic
Respond with “yes”.

Now start your application locally using heroku local, which was installed as part of the Heroku CLI.

If you’re on a Microsoft Windows system, run this:

heroku local -f Procfile.windows

Or if you’re on a macOS/Linux system, use the default Procfile by running:

heroku local

If you see “Connection in use” errors, check that no other running programs are using port 5000. On macOS Monterey, Airplay Receiver runs on port 5000 and will need to be disabled by going to System Preferences -> Sharing and then unticking “Airplay Receiver”.

Just like Heroku, heroku local examines the Procfile to determine what to run.

Open http://localhost:5000 with your web browser. You should see your app running locally.

If you see “Not Found” errors in your console, check that the collectstatic step above was run before starting the web server.

To stop the app from running locally, go back to your terminal window and press Ctrl+C to exit.

mkvirtualenv -p python3 crm