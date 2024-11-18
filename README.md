# Found - Backend

This is the backend of Found - a simplified version of [_Wellfound_](https://wellfound.com/) (previously AngelList) focused on basic candidate management from a hiring manager's point of view

## Table of Contents
* [Technologies Used](#technologies-used)
* [Project Structure](#project-structure)
* [Setup](#setup)
* [Contact](#contact)

## Technologies Used

* Python v3.11.6
* Django v5.1.2
* SQLite

## Project structure

The backend is a Django project backed by a SQLite database in a localhost environment. It has one main application, "api", that dictates/faciliates API request handling from the "Found - Frontend". Here are some of the essential structure along with useful descriptions about the "api" application:

`api/models`
* The location of the core relational models for the Found application. There are three primary models: Candidate, Interview, and Job. 
* Candidate to Interview + Job can be considered a "One-To-Many" relationship where one Candidate can have multiple Interviews for multiple Jobs. Only stipulation is a Candidate cannot have two Interviews for the same Job (i.e. a Candidate cannot be in two different interview stages for the same job). 

`api/views`
* The location of the views handling the API requests for the Found application. There are three primary Django ViewSets: CandidateViewSet, InterviewViewSet, and JobViewSet. They handle standard HTTP method handlers (i.e. 'GET', 'POST', 'PATCH', etc) along with custom method handlers like "assign_candidate_to_job" for more specialized logic.

`api/serializer`
* The location of serializering HTTP responses of the aforementioned ViewSet classes.

`api/routers`
* The location of handling the automatic construction of "URL to view" logical mapping for incoming requests. As of the time of this writing, there are only three for each of the models. 

## Setup

To setup the application server, [_npm_](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or [_yarn_](https://classic.yarnpkg.com/lang/en/docs/install/#mac-stable) are required.

1. Open your terminal and `git clone` the GitHub repository URL in your desired directory.
2. Navigate to the cloned directory with `cd <cloned_repository>`.
3. It is highly recommended to use a Python virtual environment management tool like [_pipenv_](https://pipenv.pypa.io/en/latest/) for project-specific dependencies/libraries isolation purposes among other uses.
4. Create the virtualenv (with the Pipefile) and activate it with `pipenv shell`.
5. Install Django and other necessary Django-specific dependencies with `pipenv install django django-cors-headers  djangorestframework`.
6. Run the application server with `python manage.py runserver localhost:8000`. Beyond this point, you can perform the steps detailed in the "Setup" section of [_Found - Frontend_](https://github.com/ah-berry/Found--Frontend) to get both ends running.
7. You can choose to open the application server on your browser of choice with http://localhost:8000 but there will be no route path leading to a view there. You can visit http://localhost:8000 and create a [_superuser_](https://docs.djangoproject.com/en/1.8/intro/tutorial02/) to manipulate relational objects from the Found - Frontend.

## Contact

The application was created by yours truly! Feel free to follow me on [_LinkedIn_](https://www.linkedin.com/in/ahmed-gorashi-546447b5/) and let me know if you liked using Found!