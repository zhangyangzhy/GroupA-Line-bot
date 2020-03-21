# Milestone 1 - Chatbot Design and Setup

## the Bot Type

LINE Chatbot

## the Design of Chatbot

### Module 1 - Finding Face Mask or Cleaning Substance

>Developed by 19441789 ZHANG Yang

The main purpose of this module is to provide real-time query service of stores selling face masks or cleaning substances based on users' locations, and users can also release information about stores selling face masks or cleaning substances through sending some specific message to LINE Chatbot.

There are two types of the target user in this module, one is the publisher of the store information, the other is the user who searches the store information. Users can change their roles by replying to specific keywords. LINE Chatbot will conduct different procedures according to the specific keywords entered by users, and the user can enter `"Exit"` to terminate the current procedure.

***1. For the publisher of the store information, the following functions need to be implemented:***

* **View the store information you have published**
    
    Reply to `"My Information"` to find the historical store information that you have published (each record has a unique ID).

* **Modify the store information you have published**
    
    Reply to `"Modify Information"` then enter `"Record ID"`, you can modify the attribute value by entering the corresponding attribute name, such as store name, price, quantity, and so on.

* **Delete the store information you have published**

    Reply to `"Delete Information"` then enter `"Record ID"`, you can delete the specific record you have published permanently after double-check.

* **Publish new store information**

    Reply to `"Publish Information"` then enter `"Attribute Value"` according to corresponding attribute name prompted by LINE Chabot. After confirming, you can publish this information and store the information in the Redis database. The attribute name includes the location of the store, store name, commodity type (face mask or cleaning substance), live picture, price, quantity, and other information. The location of the store can call the google map interface to obtain latitude and longitude.

***2. For user who searches the store information, the following functions need to be implemented:***

* **Search store information nearby based on your current location**

    Click `"Send Location"` button or reply to `"Current Latitude and Longitude"`, LINE Chabot will query the records within 10KM (Euclidean distance) of your current location in the Redis database, and reply to the detailed information list of nearby stores (with Record ID) order by in descending order by the released time.

* **Comment on published store information**

    Reply to `"Comment-Record ID"` then enter `"Your Comment"` to comment on store information that is not published by yourself. After confirming, the comment will store in the Redis database. If the user comments on the same record again, then it will overwrite the previous comment.

* **Rate published store information**

    Reply to `"Rate-Record ID"` then enter `"Score between 1 and 100"` can rate the credibility of store information. Credibility means whether the information about face masks or cleaning substances is accurate enough or not. If the user rates the same record again, then it will overwrite the previous score.

In terms of the Redis database, two tables will be created, one is used to store released information, the other records different users' comments and ratings on each released information.

### Module 2 - Summaries of News

>Developed by 19434405 WU Peicong

The main objective of this section is to design and implementation of summaries of news, which include three functions. Users can retrieve the latest news about the novel coronavirus through the LINE Chatbot. Also, it provides news ranking, which depends on the news recently read. Besides, users can make a favourite list to collect the news, which they interested in.

***1. Latest news***
 
* When users send the `"News"` keyword, the LINE Chatbot will send the latest news about the novel coronavirus from the Internet back to users.

* This function will consume other services.

* After that, the LINE Chatbot will send a carousel list to display the latest news. And at the bottom of each news, we can simply provide two functions, Read and Favourite.

* If users press `"Read"` button, the LINE Chatbot will return corresponding news details.

* If users press `"Favourite"` button, the LINE Chatbot will send a message to prompt users with "Saved Successful". 

***2. News ranking***
 
* Users can send chatbot `"Ranking"`, it will return a news ranking to users. That is to say after reading the news, the chatbot will count the reading time and store it into a Redis database.

* The ranking will dynamically adjust the news. For example, the life of news is only for a day. The news will be removed, which exists more than a day. Of course, if the news is valid, the ranking will base on the reading time.

* Similarly, the ranking will also provide the title of news and the reading time related to it. Users can read the news on the ranking with sending the title of news to the chatbot.

***3. Favourite List***

* If users want to see the past news they are interested in, they can simply send `"List"` to the LINE Chatbot to check out their favourite list.

* The Favourite List provide two functions. 

* One is `"Read"` button at the button of each favorited news. Similarly, if users press it, the LINE Chatbot will automatically send the details news. 

* The other is `"Delete"` button. Users can press it to remote the specific news from the Favourite List.

### Module 3 - the Measurement Against Coronavirus

>Developed by 19439822 LI Jinhui

This part of function is aiming to give people some information of measurements against Coronavirus. The chat bot may have three features. 

1. If user send one question or just one keyword to the bot, it will be able to search in the database and provide a related answer. For example. If user send "How do people measure the Coronavirus?" or "Measurement", etc, the chat bot will search related records in redis and reply the related information. 

2. The bot can provide users with basic measurements and recommendations. If user send "basic measurements", the bot will give some advice by asking several questions.
 
3. If user send a voice message to the bot, it is able to reply it.
