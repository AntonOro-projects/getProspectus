getProspectus
======
getProspectus is a service which main function is to make finding prospectus easier. The powerful search function looks through a database for all prospectus containing the search words. With the advanced search options you can choose what financial instrument you want to display, and allows you to make specific searches such as an exact match and search for a company name. With this functionality you can easily find any prospectus you need in a fraction of the time it would normally take.

**Project screencast:** https://www.youtube.com/watch?v=L6oXb9GY5rM&feature=youtu.be  
**Anton Orö individual screencast:** https://youtu.be/1IeWBhZ2Kqg  
**Rasmus Karlbäck individual screencast:** https://youtu.be/MOI7d59kKs0

## Functional specification
Features of getProspectus
* easy to use search engine for prospectuses
* login management using Google, Facebook and user credentials
* advanced search of financial instruments based on different parameters

## Technological specification
getProspectus is divided in a frontend and a backend.

The backend is a Flask application with MySQL as a data store, exposing a 
REST API. It features integrations to services including (but not limited to) 
* Facebook (OAuth2)
* Google (OAuth2)
* Finansinspektionens Prospektregister (if possible)

Directly visible to the user, the frontend fetches data, partly from the getProspectus 
API, partly from services such as
* Facebook (OAuth2)
* Google (OAuth2)

The frontend is using React and Redux.

