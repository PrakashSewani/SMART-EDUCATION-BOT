# SmartEducationBot
This Bot is a PDF-Scrapper, meaning it can fetch answers from the provided PDFs which are parsed into text files.


![image](https://user-images.githubusercontent.com/81285705/166434842-532d17ff-133e-4f1d-898c-59d4be0b15d5.png)


This is the flow of my project, The User Query is fetched and passed onto the YAKE! Module which extracts the keywords from the Query. These keywords are then passed on to the Context Identification Module, which returns the context as well as the User Query into BERT Module. Produced answer can be liked or disliked by the user.


![image](https://user-images.githubusercontent.com/81285705/166435147-5b96008e-6033-4da0-9648-55c972674a5e.png)


If the user dislikes the answer, the Query is then passed onto the Web-Scrapper Module which returns the Answers provided by Google.


![image](https://user-images.githubusercontent.com/81285705/166435256-659306f9-f0fe-4fe3-b532-c12e5ec606e0.png)
