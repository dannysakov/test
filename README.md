# <u>  Website for librarian :mortar_board: </u>

Hello, on the following site you can do a number of things to run a small library

### What can be done on the site?
 - Adding new customers and books
 - Borrowing books as well as returning them by existing customers
 - Deleting existing customers and books
 - Search for customers and books by their name
 - Three ordered tables of the book customers and the existing loans.
Each table has all the information on that subject
 - In addition, there is a table that shows the loans that were not returned on time 


 ### Things for the developer

 1. There is an option to delete all the tables, I didn't put it in the main code so that there is no situation where all the information on the site will be accidentally deleted  If you want the additional code, you can send me an email to - dannysakov123@gmail.com

 2. The site is built from a main Python file.

 3.  there is a folder called "templates" in which there are all the html files that are connected to Python

 4. There is a html layout page that connects all the pages

 5. And there is a folder called "static" in which there are all the css files that are connected to the relevant html files

 6. <span style="color:red">  The loan table on the server side has the id of the clients and the books id , on the other hand, on the client side there are the names of those books and clients so that even those who do not understand programming can operate the site and so there will be less confusion and mistakes</span> 

 
### Things for improvement or future programming :smile:

1. Added another button for adding book images.

2. Added a button to delete the loan despite the delay

3. Add a little more style to the pages themselves

4. Add a code from the main page so that not everyone can log in and make changes to the site

5. Make a loan extension option

6. Add an identity card or something similar so that it does not create a situation of similar customers

7. To connect certain functions and transfer additional information so that it is not necessary to refresh certain pages for the information to appear again

8.  make another column in the loan table in which it is written that the book is still in the loan period or that it has already passed this date   (That is, instead of a column for the actual return date, there will be a column for whether or not the book was returned. And make a change in the places where the python code calls the actual return column will call the new column)
