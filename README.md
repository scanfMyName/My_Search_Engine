# My_Search_Engine

I have completed this project by dividing it into 2 components those are:-

1. To get the question text files, their title and respective links for each question we have done web scraping in python using modules like beautifulsauce selenium, 
web driver manager and then we go for finding the keywords present in the whole corpus. After that we go for making the tfidr matrix and then we store it in a txt file.

2. Now we will be setting up a node app that will be setting its frontend using the ejs files. We will be using the keyword extractor module for the query available in node and then we willbe using the tfidr matrix that we have created in the previous component and suing the cosine similarity rule we go for finding the 10 best possible result for queryand send them to front end to show them in a list wise manner. Now for each result we need also to show the whole question and the corresponding link of the question from where we have extracted that question, so we make a new api for that that is "/CompleteQ/:q_id" and in this we will be showing the question of the corresponding search result.   