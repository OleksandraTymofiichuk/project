# Snyatyn Press
#### Video Demo:  <https://youtu.be/LQAeHaY3AAU>
#### Description:


# About the project
My name is Oleksandra Tymofiychuk, I am from Ukraine, from the city of Snyatyn. For my final project, I implemented the idea of ​​creating a web application using JavaScript, Python with the Flask framework, and SQL.
It is called "Snyatyn Press", which allows users to view and read news articles with the ability to change the theme of the website to night or day modes.
For registered users, the following functions are available: creation of news articles, editing, deletion, as well as entering and editing additional information in your personal data profile.

# Project structure
The project is placed in the "project" folder. Which consists of folders: "static", "templates" and files "app.py", "project.db", "requirements.txt", "README.md".
* "static" - images that the user uploads to the site are stored here and also contains the "java script" folder with the "theme.js" file, which changes the site's themes from day to night and vice versa.
* "templates" - all html pages are contained here.
* “app.py” is the main application code file.
* "project.db" is a file that stores information from the database.
* "requirements.txt" is a text file with the listed libraries used in the program.
* “README.md” is this explanation file.

# Functionality for unregistered users
And now more details about the functionality.
* An unregistered user will immediately go to the main page of the site via the link, where blocks with news are displayed using cards from Budstrap. These blocks contain five fields for displaying the title of the article, the main part of the text, a photo, the date and time of creation and the author of the article. The first 169 characters of the article are displayed in the text field.The header is a link that can be used to go to the next html page for a full view of this article. After reading the entire article, the user will return to the main page by clicking the "Snyatyn Press" button. There are also three more buttons in the top menu: “Register”, “Log in” and icons with images of the sun or moon.

* The "Register" button redirects to another html page where you can register on the site. The page contains a form consisting of three input fields (username, password, password confirmation) and a "Register" button that sends the entered data from the form. During registration, validation is implemented, which intercepts possible errors, such as: unfilled fields, entering a name that already exists in the database, and password mismatches in the fields. If an error occurs, a flash message appears with the error text on a red background and returns to the same registration page.After successful registration: the data is recorded in the database, the user is redirected to the main page, the user ID and name are recorded in the session and the name is displayed in the top menu.

* The "Log in" button redirects to another html page where you can log in to the site. The page contains a form consisting of two input fields (username, password) and a "Log in" button, which sends the entered data from the form. Validation is also present, as well as a check of data matching with the database. After a successful login, you are redirected to the main page, the user ID and name are recorded in the session and the name is displayed in the top menu.

To develop the project, I created two tables in the database. Table "users" with columns: id , username , hash , date_of_birth , phone , email , address. Found "news" with columns: id , users_id , datetime , header , text , image . The date and image columns are filled by default.

# Functionality for registered users.
 After successful registration or login:
* the "Register" and "Log in" buttons disappear, and "Log out" appears, which clears the session data and displays the main page of the site, as for an unregistered user.

* the "Add news" button appears, which redirects to a new html page with a form that has fields for writing the header, main text, and a button for downloading a file from the user's computer in .jpeg, .jpg, .png format. After confirmation of sending data, validation takes place for filling in the text fields. If successful: the name of the image is hashed, a path for storing the photo is created and stored in the “static” folder.The information of the title, text, new name of the image, author's name from the session, date, time is inserted into the database. Redirects to the main page, which displays an additional news item at the top and a “flash” message on a green background with text about success.

* If you view your own news in full size by clicking on the title, you can edit and remove the news using the "edit" and "remove" buttons. This form contains a hidden field containing the news ID. When editing, a page appears with a form that is similar to the page for creating news, but with filled fields and the display of the current photo. You can save the changes using the "save" button, which updates the information in the database table with this news according to the news id contained in the hidden field.

* When deleting a news item, a modal window appears with two buttons to confirm or reject the intent. After confirmation, the news item is deleted from the database and is no longer displayed when redirected to the main page.

* When you click on your name in the top menu, a page with five fields for entering information, a hidden field with user ID data according to the session and a button to save changes is displayed. With each click, the current information from the database about the user will be displayed in the fields.Validation for the name field is present here to prevent the field from being sent empty or from selecting a name that already exists in the database. As well as validating the correct format for the phone and e-mail address fields.

Changing the theme of the site is implemented using JavaScript using four functions. When you click on the moon icon, the background color becomes dark, the text color becomes light, and the frame becomes blue. And the moon icon disappears, and the sun icon appears. When you press the sun, the opposite happens. This property is saved when switching between pages of the site.