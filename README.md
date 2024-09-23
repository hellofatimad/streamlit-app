## How to use

### Update the streamlit/app/.streamlit/secrets.toml file
[connections.snowflake]
account = "IDENTIFIER" // Be sure to change the . to - in your account identifier
user = "USER"
password = "PW"
role = "ACCOUNTADMIN"
warehouse = "WH"
database = "DB"
schema = "SCHEMA"
client_session_keep_alive = true

### Run Command
cd app
streamlit run main.py

### Pages
Before:
- Make sure to refresh a couple of times to bypass the st.set_config() error

main.py
- Calls all of the functions from other .py files 
- Sets up the pages and interface

login.py
- Creates a login and register interface
- User authentication is basic, mainly compares the username and password from Snowflake
- Potential Improvements to Test: 
    * Use hashing for either username or password to create a more secure user authentication system
- Includes the logout function

home.py
- When the user logs in, the app defaults to the user to the checklist feature
- Checklist feature connects with your Snowflake DataBase:
    * Add
	* Read
	* Update (Edit)
	* Delete
- Potential Improvements:
    * Create cards or tags for specific checklists?
    * Implement timeline: <https://pypi.org/project/streamlit-timeline/>

snow_db.py
- This is for the snowflake database functions
- Used for home.py

breast_cancer.py
- Uses logistic regression to predict breast cancer
- Functions that help with the interface such as sliders, radar chart, and more
- Reads from the pickle file in streamlit/model/breast_cancer.py
- 'Pickle files write' converts Python objects to bytes 

patient_experience.py
- Uses random forest classifier to predict patient care experience
- Mimics the interface and functionality of breast_cancer

form.py
- Allows users to play with their data
- Exploratory Data Analysis
- Potential Improvements:
    - Add more graph options: boxplot, etc.
    - Create a 'duplicate' container to deal with duplicates

laboratory.py
- Uses an open source streamlit component
- Allows users to test their code

settings.pu
- Uses logout function from login.py
- Potential Improvements:
    - Create other functions such as changing themes of the overall app!

## Additional Notes:

### Data
All of the data are pulled from Kaggle!