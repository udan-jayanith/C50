# What is this project?

This web app is called **URL Manager**. It allows users to store and organize URLs efficiently.

URLs are stored inside **Libraries**, which are collections of URLs. Users can name these libraries, add descriptions, and set a visibility mode — either **private** (only the creator can access it) or **public** (anyone can view the library and its contents).

When a URL is saved, a timestamp is stored to indicate when it was added. Users can also provide a custom title for the URL. If no title is given, the application attempts to fetch the title from the URL itself. If that fails, the backend returns an error prompting the user to enter the title manually.

When a user logs in, a default library called **"My Urls"** is automatically created if it doesn't already exist. Users can edit or delete any URL or library they’ve created.

# Distinctiveness and Complexity

My final project is built using Django, HTML, CSS, and JavaScript without relying on Bootstrap. Skipping Bootstrap made development more challenging, but I still managed to create a clean and user friendly UI/UX.

I’ve implemented several custom Django models, including the use of ManyToManyFields, and the backend includes user input validation for security. The app also uses a CSRF token and contains model methods to keep the code efficient and clean.

On top of that, I integrated two external libraries for web scraping functionality.

The web app is mobile responsive, tested with Chrome DevTools, and has a unique interface tailored specifically for this project.

On the frontend, I implemented infinite scrolling, allowing new content to load seamlessly as the user scrolls (no button clicking needed). I also used HTML templates and the built-in <dialog> element, which are relatively modern features in HTML and JavaScript.

This project also has a status bar that appears when there's a onging http reqeust to the backend.

---

# Pages

This project includes 3 main pages:

- **Libraries Page**  
  Shows all the libraries a user has created. If the logged-in user is viewing their own profile, it includes options to create a new library and displays both public and private libraries. For other users, only the public libraries are visible.

- **Library Page**  
  Displays all URLs within a specific library. If the user is the owner, they are given options to edit or delete URLs or the entire library.

- **Public Libraries Page**  
  Lists all publicly available libraries across the platform.

---

# What’s contained in each file I created

## `URL_Manager/`
Main project folder.

- **`urls.py`** – Declares all application routes and links them to view functions.

- **`views.py`** file contains about 12 functions. This file containes most of the project backend code. This contains 3 functions top of the page for authentication as usual. And the index function serves public libraries page if the user is not authanticated. Else it servers My URLs libraries page of the user. getTitle function take a url and return it's title. These are several functions in this file and there are more functions in this file.

- **`models.py`** file contains 4 models. And the User model is a Abstract User class in Django. Profile model stores user data i have implemented for this project. And other two models which are URL and Library as name suggest those modeles are used to store url data and library data.
---

## `URL_Manager/templates/`
Contains HTML templates used by Django.

- **`layout.html`** – The base layout used by all pages (includes navbar and structure).

### `URL_Manager/templates/libraries/`

- **`libraries.html`** – Template for the Libraries page.
- **`library.html`** – Template for individual Library pages.
- **`publicLibraries.html`** – Template for the Public Libraries page.

### `URL_Manager/templates/authentication/`

- **`login.html`** – Login page template.
- **`signin.html`** – Sign-up page template.

---

## `URL_Manager/static/`
Contains all static assets: CSS and JavaScript.

### `URL_Manager/static/scripts/`

- **`script.js`** – Shared JavaScript used across all pages. And this file contains CSRF token handeling logic, custom scorlled event in body-container class. And status bar functionalities.


### `URL_Manager/static/scripts/libraries/`

- **`library.js`** – JavaScript for the Library page (e.g., URL actions).
- **`libraries.js`** – JavaScript for the Libraries and Public Libraries pages.

Both files above are responsible for rendering and making requests to the backend. And both files implement infinite scrolling to the page.

### `URL_Manager/static/styles/`

- **`style.css`** – Global styles and application theme. Also includes utility classes for layout and design.
- **`statusLine.css`** – Styles for the bottom status bar that displays during network requests.
- **`nav.css`** – Styles for the navigation bar.

### `URL_Manager/static/styles/libraries/`

- **`library.css`** – Styles specific to the Library page.
- **`libraries.css`** – Styles for the Libraries and Public Libraries pages.

### `URL_Manager/static/styles/authentication/`

- **`style.css`** – Styling for the login and signup pages.

# How to run this application

If your a Unix(mac and linux) user use python3 instead of py.
Before running the scripts below make sure you have installed necessary python packages.

`py manage.py makemigrations URL_Manager`\
`py manage.py makemigrations`\
`py manage.py migrate`\
`py manage.py runserver`

In case any error occurred try deleting db.sqllite3, migrations folders and cache folders and run scripts above.
