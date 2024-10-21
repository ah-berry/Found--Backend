# Wellfound Clone - Backend

This is the backend of the Wellfound Clone - a simplified version of Wellfound (AngelList) focused on basic candidate management from a hiring manager point of view.

## Table of Contents
* [Technologies Used](#technologies-used)
* [Project Structure](#project-structure)
* [Setup](#setup)

## Technologies Used

* Python v3.11.6
* Django v5.1.2
* SQLite

## Project structure

The backend is a Django project backed by a SQLite database in a localhost environment. It has one main application, "api", that dictates/faciliates API request handling from the "Wellfound Clone - Frontend". Here are some of the essential structure along with useful descriptions about the "api" application:

`api/models`
* The location of the core relational models for the Wellfound Clone application. There are three primary models: Candidate, Interview, and Job. 
* Candidate to Interview + Job can be considered a "One-To-Many" relationship where one Candidate can have multiple Interviews for multiple Jobs. Only stipulation is a Candidate cannot have two Interviews for the same Job (i.e. a Candidate cannot be in two different interview stages for the same job). 

`api/views`
* The location of the views handling the API requests for the Wellfound application. There are three primary Django ViewSets: CandidateViewSet, InterviewViewSet, and JobViewSet. They handle standard HTTP method handlers (i.e. 'GET', 'POST', 'PATCH', etc) along with custom method handlers like "assign_candidate_to_job" for more specialized logic.

`api/serializer`
* The location of serializering HTTP responses of the aforementioned ViewSet classes.

`api/routers`
* The location of handling the automatic construction of "URL to view" logical mapping for incoming requests. As of the time of this writing, there are only three for each of the models. 