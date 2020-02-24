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

The main objective of this section is to design and implementation of summaries of news, which include two functions. One is the least news from the Internet. When users send the news keyword, the chatbot will send some news at present back to users. Another is the top 5 news among all the news, which have been read recently. That is to say after reading the news, the chatbot will count the reading time. When we send the chatbot with hottest keyword, it will return us the top 5 news according to the recent reading records.

### Module 3 - the Measurement Against Coronavirus

>Developed by 19439822 LI Jinhui

This part of function is aiming to give people some information of measurements against Coronavirus. The chat bot may have three features. 

1. If user send one question or just one keyword to the bot, it will be able to search in the database and provide a related answer. For example. If user send "How do people measure the Coronavirus?" or "Measurement", etc, the chat bot will search related records in redis and reply the related information. 

2. The bot will remember how many times each answer used and provide a rank list. 
 
3. If user send a voice message to the bot, it is able to reply it.
