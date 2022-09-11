# supercapacity

## About
This project was created in the process of participating in the [hackathon](https://ai.itmo.ru/dataproducthack)
 on the Biotech track. In this project, we are trying to predict the capacity of supercapacitors depending on the synthesis parameters.
Structurally, the project consists of [data](https://docs.google.com/spreadsheets/d/1hMohZ1m7PjKro6NAdXuMZ854H_L0KN6Z9Z8SgwzjdpY/edit?usp=sharing) obtained from scientific articles, a model trained on this data, a backend on Django, and a frontend on Rshiny.  

This project is the winner in the Biotech track.

## Data policy
If you came to this page in search of [data](https://docs.google.com/spreadsheets/d/1hMohZ1m7PjKro6NAdXuMZ854H_L0KN6Z9Z8SgwzjdpY/edit?usp=sharing), and you want to use it - you're welcome, we're glad that someone needs it. Put a star!
## Team
 * Alexandra Korneeva (alexandraroots) - TeamLead/ML + Data collecting
 * Dmitry Vedenichev (PopeyeTheSailorsCat) - Backend + Data collecting
 * Pavel Petrov - Frontend + Data collecting
 * Valentina Bocharova - Chemist/Product + Data collecting  
## Project structure
 The project contains 4 main parts: Data, a trained model, a backend for the model host, and a frontend for interacting with the model.
 * Backend: Docker+Django. API by restframework.
 * Frontend: Rshiny, hosted on rshinyapps.io (тут ссылку пихнуть).
 * Model: boost model trained on data.
 * Data: Google excel Table.

## Future development
* Backend:
  * Fix the problem created by Docker when changing the model code. Docker notices the change, updates the code and writes it as a new model to the database. However, the register knows only one model, and their id usually does not match, which causes the server crash problem. To create this problem, it is enough to remove the crutch.
Located supercapacity_api/view.py: algorithm_object = registry.endpoints[algs[len(algs)-1].id]
  * Fix crutches created as a result of lack of time to study. An example would be model_name and model_rename_predict in ml.income_classifier.dummy_model.
  * Make the same logic work for prediction and optimization.
  * Refine the logic of working with the model.
* Model:
  * Do not use pandas.
  * Add the ability to capture reagents, or remember reagents from previous calls (probably even the second, in the case of multiple requests to the server). Perhaps you should put the logic of requests to chemical services in a separate class.
  * Rework the logic of working with the rest of the application. It is possible to get dictionaries for prediction and work with them - it will simplify the life of the backend.
  * In general, optimize the operation of the model in time.
  * Add a classification of the final structure.
* Front:
  * It's beautiful :*
  * Stop randomizing the final structure.
* Future:
  * Host project on server.
  * Add additional training from the data in the table, after a certain period of time.
  * ???

