# DIS project 2024
 
# I) HOW TO COMPILE THE WEB-APP FROM SOURCE:

Download all the files from the GIT repository into the same folder on your harddisk.

Initially create a new database in pgadmin or psql. By default we have called this database "order_project", but you can decide another name. If you decide to use another name for the database, then you have to change the database name on line 10 in the python file project.py. 

By default we have called the database's user 'postgres', its host 'localhost', and its password '12345'. You are free to set any of these variables to other values. But if you do so, please make the appropriate changes on line 10 in the file dis_proj.py.

After the database has been constructed, the schemas of the relations have to be defined. We also load a few tuples into these relations to test if the relations work in a desirable way.
This is done by the sql file schema.sql. Go to the sql file's folder in a normal command prompt and run: psql -U postgres -d order_project -f schema.sql.
(It is assumed that you have access to run the psql program from whatever folder you are in.)

Futhermore, you need to have the necessary python packages installed. Go to the subfolder where the file "requirements.txt" is located, and run in either a Developer Command prompt or a shell in a terminal in Visual Studio Code(VSC) : pip install -r requirements.txt
This installs all the packages you need.

Now the program should be able to run. 

# II) HOW TO RUN AND INTERACT WITH YOUR WEB-APP:
RUN:
####
If I) has been done, then you are ready to run the web-app. In a normal command prompt go to the folder where the python file project.py is located and run: python project.py
This will run the python file. The python file needs to run like this all the time you want the webpage to run. If you want to stop the program, then go to the command prompt where the program is running and enter CTRL-C.

Open your internet browser and type the following address into the address bar in the browser and press Enter: http://127.0.0.1:5000
Then you should be at the front page of the web-app. 

INTERACTION:

On the front page of the web-app you can decide to either login and choose to use a username that has already been created or create a new username and decide a budget. 
When you have either logged in or created a new username, then you also have a budget, and then you can proceed to making your order. You order first your burger, then you order your beverages, followed by ordering your french fries, and ending with ordering your desserts. 
Finally, your full order will be presented to you. You can now decide to delete some of your orders, which reduces the total purchase sum by the price of the deleted orders. When you have deleted all the order items you want to delete from your order, you submit the order. Your budget will then be reduced by the total purchase sum, and this will be evident for you next time you log in using the same username. 
In the immediate final step you can choose to either return to the front page of the web-app - and again decide to either login or create a new user - or to write a complaint. If you press the complaint button, you will transfer to a new webpage where you can write a complaint. You should leave your phone number as part of the complaint. Only 8-digit phone numbers will be accepted.

REGULAR EXPRESSION:

A regular expression will match the 8-digit phone number in the written complaint, and a new tuple (orderid, complaint_text,phonenumber) will be inserted into a relation called Complaints. Since these complaints should not be accessible for the customers, this relation will not be accessible from the webpage, but only from employees at the restaurant who can access it using a SELECT SQL commands in e.g. pgAdmin or another database program. 
If you want to see the tuples in the Complaints relation, then run the following line in pgAdmin: SELECT * FROM Complaints.
