# Chatbot README

# PROJECT DESCRIPTION

The main goal of this project is to produce a secured  and privacy Q & A bot  for Network security course. Unlike  other bots, our bot is exclusively on local machine. Our bot is capable of answering questions which are related to network security course. Our bot is a user friendly interface  which provides a user-friendly interaction. Users can easily give the input questions and bot gives accurate and relevant answers It prioritize’s   privacy of the data by keeping all information on local machine.Data in bot is stored locally to eliminate internet issues.Bot is specialized in providing answers related to Network security documents.

# System Architecture
![image](https://github.com/sheshiisree/Q-A-bot/assets/147757630/994a3659-30cd-4140-a2f1-4a1f4a790c69)


## Installation

To install the required packages for this project, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

## PDF Loader
Before running the Flask app, make sure to add the required PDF file(s) to the ./data directory.

Execute the following command to load the PDF data:

```bash
python pdf_loader.py
```
This command will handle the loading of the necessary PDF files into the app.

## Flask App
Start the Flask app by running:
```bash
python app.py
```
Visit http://localhost:5000 in your web browser to access the application.
