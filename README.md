Guide to run this locally
setup your own virtual environmet
install the requirement.txt packages via pip install -r requirements.txt
setup api key via open router
and setup OPENWEATHER_API_KEY
LANGCHAIN_API_KEY 
have these api keys in your .env 
after alll this setup you can run the application via 
streamlit run streamlit_app/app.py
u can check langsmith evaluation via your dashboard

Run unit tests:
pytest -v tests/
Add a documenment for rag funcunality and u can chat for realtime weather updates have used both free api keys so limited functionalities  are there 
