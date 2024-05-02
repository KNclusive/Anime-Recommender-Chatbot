# Anime-Recommender-Chatbot
The Repository Includes codes and details about Anime Recommender Chatbot. This is an NLP-IR collaboration

This Project Involves Two parts:
* Front-End for User Interaction with Chatbot (Uses Flask to create ).
* The Recommender which is an combination of Content and Collaborative filtering techniques (Meta Approach-Switching Hybrid)
* Also an Conversation pre-trained bot from Microsoft i.e DialogBOT is used to create coherent and fluent conversation.

I will now proceed to give detailed explanation the project.

## Front-End
The file Chatbot_Flask.ipynb is the main code which runs the project, It launches the local host server using which user can interact with the recommender system. The front-End UI is made using HTML and CSS code which are the files "chat.html" and "style.css" respectively (Files need to be present in local system).

## Recommender
This Part is also present in the file Chatbot_Flask.ipynb. This part contains multiple interactive functions like:
* initial_chatting : to get user initialized and collect basic information like user_name or content information if user data is un-available while creating new user in system.
* memoizing_chat : creates an memoized chat function which retains history of chat and sequence which imparts an flow of information.
* get_chat_response : This function is used to enable the conversations with the pre-trained bot from microsoft for coherence and fillers
* Google_drive_data_load : Uses file "Google_Drive_Credentials" for Accessing the Databases from Google Drive, Making the project Device Agnostic.
* load_model_from_memory and list_and_load_models : Used for enabling Multi-threading approach in so that data loading from Drive becomes a parallel process on multiple threads each establishing its own service to Google-Drive.
* generate_profile_name : To create an user_name for new users
* Finally the most important function "memoized_Chat" Which creates the flow of conversation and toggles between "Content Filtering" and "Collaborative Approach" based on boolean flag setting methods and sequence record.

There are two additional files that are used to enable the recommendation process namely:
* response.py : Uses Text Construct API from OpenAI used for :
  * Classifying Intent from User Query like "Anime-Name", "Genre", "Number of Episodes" etc.
  * Also used to Create Fluent continuous text from retrieved data.
* recommend.py : Contains Functions like:
  * collaborative_main : for Collaborative filtering approach uses function like "distance_weights" for User weighing / priority classification and "roulette_selection" for anime selection based on User Similarity.
  * Content_main : Querying on database with expressed content and return data which satisfies all-condition or any-condition criteria with priority to "ALL".
  * popular_main : Handles Cold_Case senario where neither User is found ruling out the Collaborative Approach nor any specific content requirement is expressed which rules out content filtering as well but recommendation is still asked.

Note: The entire project Works on Using .Joblib Files which are used to store pre-calculated Distances and Pre-trained KNN models for Similarity claculation. Also "Trainer.ipynb" file is being attached which trains the KNN models and stores data like user_item matrix, user_data, rating_data, item_data, combined-features embeddings for content filtering etc. This trainer is to be called when new user is created or the user updates the rating for an anime or provides new rating for a particular anime. (The updation and creation of user and item data in not included in the project currently but can be considered for Future scope.)
