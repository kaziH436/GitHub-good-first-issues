import streamlit as st
from pymongo.mongo_client import MongoClient
import os
import time
from dotenv import load_dotenv, dotenv_values
load_dotenv()


st.set_page_config(
    page_title="GitHub Good First Issues Tracker",
    page_icon=":)",
    layout="wide",
    initial_sidebar_state="expanded",
)

# load mongoDB password 
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_uri = os.getenv('MONGODB_URI')  # Should be complete connection string from MongoDB Atlas
database_name = os.getenv('MONGODB_DATABASE', 'github_issues')  # Default value provided
collection_name = os.getenv('MONGODB_COLLECTION', 'issues') 


# Connection to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# load data from mongoDB
def load_data (page_size, page_number):
    skip_value = page_size * (page_number - 1)
    return list(collection.find().skip(skip_value).limit(page_size))
    
# Display data
def display_data (record):
    issue_title = record["issue_title"]
    repo_name = record["repo_name"]
    issue_url = record["issue_url"]
    label_name = record["label_name"]
    label_url = record["label_url"]

    st.markdown(f"## {issue_title}")
    st.link_button(repo_name, f"https://github.com/{repo_name}", type = "primary" )
    st.markdown(f"**Issue URL** : {issue_url}")
    
    st.link_button(label_name, label_url)

    state_indicator = "🟢" if record["state"] == "open" else "🔴"
    locked_indicator = "True" if record ["locked"] else "False"
    st.write(f"**Status:** {state_indicator}  **Locked:** {locked_indicator}")
    
    st.markdown ("---")

# Streamlit App
def main():
    st.title("Github Good First Issues - GHW")

    #  Pagination Settings
    page_size = 20 
    page_number = st.sidebar.number_input("Page Number", min_value=1, value=1)
    total_records = collection.count_documents({})
    st.sidebar.write(f"Total Records: {total_records}")
    # loader while fetching data
    with st.spinner ("Loading..."):
       time.sleep(5)
    # load data
       data =  load_data(page_size, page_number)
       for record in data:
        display_data(record)

if __name__ == "__main__": 
 main()