# BOOKAHOLICS 
#### Video Demo:  <URL https://www.youtube.com/watch?v=wFdISG-M8z4>
## Description:
### 1. Ideas
#### I love reading books. But I usually forget the contents and my thoughts after reading after a while. I made this website so that people like me can simpply record what they read.
### 2. Overall Structures
#### There are 3 things you can do: make a new entry, see your past entries and look at what users of this website have read.You can also do a search by enterning keywords at this page.
### 3. Detailed functions of each page
#### 3.1. Index Page
#### There are two main features here. New users can register with username, password that are least 6 characters long. There will be alerts at the input fields if username and password do not meet this requirement. After getting the registeration information, I then use a hash function to hash the passowrd to before storing it in the database.
#### Another feature is for existing users to log in. When they click on the log in button, a form will pop up.
#### 3.2. Login Page
#### New users are directed to this page after they successfully register. They need to fill in their log in information.
#### 3.3 Loggedin Page
#### After logging in, users will be directed to this page where they have 4 options: make a new entry, see thei past entries, see what users on this website have read randomly and do a search for entries that contain the keyword they enter.
#### 3.4. New Page
#### Here users can enter new entries about the books they read. I achieve this by creating a form where they type in all information about title, author, genre, review, time they spent on reading the book. They can give star rating to the books. 
#### 3.5 Past Page
#### Here are all the past entries of an user display in a table form. They only see a few things about the entry here. This page is also used to show random entries.
#### 3.6 Entry
#### This page is to show all the details of one entry. (The user goes here by clicking on "Read the full entry" button next to each entry in the past entries list or the random entries list).
### 4. Detailed designs
#### 4.1 CSS
#### I used a CSS file in static to style all the elements in my website. The style I chose is minimalist so the range of fonts and colors are limited. Every page of the website has a background photo that is related to books. The text is center-aligned.
#### 4.2 Javascript
#### I used Javascript to dymamically create page numbers for the past page. The number of entries shown on each page is limited by 3 and if the total number of entries exceed that, page numbers will automatically be created.
### 5. Database
#### I used SQL to create 2 tables to store data. The first one is to store users' information which has 2 columns of username and hash. 
#### Another table is to store entries that users record. There are a total of 7 columns, coressponding to the form in the new page. 
