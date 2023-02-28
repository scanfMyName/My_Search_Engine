# Web Search Engine Based on TF-IDF Algorithm

This project is a web search engine that is based on the TF-IDF algorithm. It allows users to search for Data structure and algorithm questions from Leetcode and returns the most relevant results based on their queries.

## Getting Started

To get started with the project, you will need to follow these steps:

1. Clone the repository to your local machine.
2. Create a Pycharm project on your local machine with main.py file and vitual environment in it, and copy the code as what written in the main.py file in the cloned project.
3. Install the required dependencies for the main.py file(or as mentioned below) in the virtual environment.
4. Run `main.py` to fetch questions from Leetcode, scrape their links, and store the questions in text files and scrap the question texts and generate tfidf matrix.
5. Now copy all the files, that you get by running the main.py file inside the folder where your node app or server.js file residing.
6. Now move to your terminal at the folder where 
7. Run `npm install` to install the required modules for the Node.js application.
8. Run `npm start` to start the Node.js application.
9. Open your web browser and go to `http://localhost:3000` to access the web search engine.

## How to Use

Once the web search engine is running, you can type or speak your query or question in the search box. The engine will apply lemmatization and generate a simple query text. It will then use cosine similarity to find the most relevant questions from the TF-IDF matrix and display them in the search results. You can click on a question to view its full text and link to the original question on Leetcode.

## Dependencies required to install for main.py file to run

- bs4
- math
- numpy
- nltk
- string
- Selenium
- webdriver_manager


## Dependencies

- Python 3.x
- PyCharm
- Node.js
- Express
- EJS

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
