from flask import Flask, render_template, redirect, url_for, session, request, flash
import psycopg2
import os
import queries
import re

app = Flask(__name__)

# Set your own database name, username, and password
db = "dbname='order_project' user='postgres' host='localhost' password='12345'"

conn = psycopg2.connect(db)
cursor = conn.cursor()

@app.route("/", methods=["POST", "GET"])
def home():
    if 'userid' in session:  
        userid = session['userid']
        budget = queries.select_budget(userid)
        return render_template("user_page.html", userid=userid, budget=budget)
    return render_template("frame.html")

@app.route("/createaccount", methods=['POST', 'GET'])
def createaccount():
    cursor = conn.cursor()
    list_users = queries.select_budgets_and_usernames()
    cursor.execute('''SELECT COUNT(userid) FROM users''')
    number_of_users = cursor.fetchone()[0]
    cursor.close()
    if request.method == 'POST':
        new_username = request.form['username']
        new_budget = request.form['budget']

        if queries.insert_user(new_username, new_budget):
            return redirect(url_for('home'))
        else:
            flash("Your username is already in use by another person. Try another username!")
    return render_template("createaccount.html", users=list_users, number_of_users=number_of_users)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        users = queries.select_usernames()
        return render_template("login.html", users=users)

    if request.method == "POST":  
        username = request.form['username']
        user = queries.select_userid(username)
        if user:
            # save userid in session
            session['userid'] = user
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))


@app.route("/order1_burger", methods=['GET', 'POST'])
def order1_burger():
    if request.method == 'POST': 
        orderid = session['orderid']
        budget = session['budget']

        burger_type = request.form['burger_type']
        patty_type = request.form['patty_type']
        bun_type = request.form['bun_type']
        amount = request.form['number_of_burgers']

        # Determine price based on burger_type
        if burger_type in ["Classical style", "Kids Choice"]:
            price = 30 * int(amount)
        elif burger_type == "Cheese Burger":
            price = 35 * int(amount)  
        elif burger_type == "Goat Cheese":
            price = 45 * int(amount)  
        queries.insert_burger(burger_type, patty_type, bun_type, orderid, price, amount)

        if request.form['action'] == 'next':
            spent = float(request.form['spent']) + float(price)
            return render_template("order2_beverage.html", orderid=orderid, budget=budget, spent=spent)
        elif request.form['action'] == 'extra_burger':
            spent = float(request.form['spent']) + float(price)
            return render_template("order1_burger.html", orderid=orderid, budget=budget, spent=spent)
        
        return render_template("order2_beverage.html", orderid=orderid, budget=budget, spent=spent) 
    
    # Create a new order for the new user
    if not session.get('orderid'): 
        userid = session['userid']
        new_orderid = queries.insert_order(userid)
        session['orderid'] = new_orderid
        session['spent'] = 0
        budget = queries.select_budget(userid)
        session['budget'] = budget
    
    orderid = session['orderid']
    spent = session['spent']
    budget = session['budget']
    return render_template("order1_burger.html", orderid=orderid, budget=budget, spent=spent)

@app.route("/order2_beverage", methods = ['POST', 'GET'])
def order2_beverage():

    if request.method == 'POST':  
        orderid = request.form['orderid'] 
        budget = request.form['budget'] 
        spent = request.form['spent']     
        beverage_type = request.form['beverage_type']
        volume = request.form['volume']
        number_of_beverages = request.form['number_of_beverages']
        
        # Determine price based on burger_type
        if beverage_type in ["Coca Cola", "Pepsi"]:
            price = 20
        elif beverage_type == "Tuborg pilsner beer":
            price = 40
        elif beverage_type == "Heineken beer":
            price = 50
        price = int(number_of_beverages) * int(price)
        # insert into beverage and food table
        queries.insert_beverage(beverage_type, volume, orderid, price, number_of_beverages)
        if request.form['action'] == 'next':
            spent = float(request.form['spent']) + price
            return render_template("order3_french_fries.html", orderid=orderid, budget=budget, spent=spent)
        elif request.form['action'] == 'extra_beverage':
            spent = float(request.form['spent']) + price
            return render_template("order2_beverage.html", orderid=orderid, budget=budget, spent=spent)
        elif request.form['action'] == 'back':
            return render_template("order1_burger.html", orderid=orderid, budget=budget, spent=spent)


@app.route("/order3_french_fries", methods = ['POST'])
def order3_french_fries():
    if request.method == 'POST':
        orderid = request.form['orderid']
        budget = request.form['budget']
        spent =  request.form['spent']

        french_fries_type = request.form['french_fries_type']
        french_fries_size = request.form['french_fries_size']
        number_of_french_fries = request.form['number_of_french_fries']
        
        # Determine price based on french_fries size
        if french_fries_size == "Small":
            price = 20
        elif french_fries_size == "Medium": 
            price = 30
        elif french_fries_size == "Large": 
            price = 40
        elif french_fries_size == "Extra Large":
            price = 50
        price = int(number_of_french_fries) * int(price)

        # insert into french fries and food table
        queries.insert_french_fries(french_fries_type, french_fries_size, orderid, price, number_of_french_fries)
        if request.form['action'] == 'next':
            spent = float(request.form['spent']) + price
            return render_template("order4_dessert.html", orderid=orderid, budget=budget, spent=spent)
        elif request.form['action'] == 'extra_frenchfries':
            spent = float(request.form['spent']) + price
            return render_template("order3_french_fries.html", orderid=orderid, budget=budget, spent=spent)
        elif request.form['action'] == 'back':
            return render_template("order2_beverage.html", orderid=orderid, budget=budget, spent=spent)        


@app.route("/order4_dessert", methods = ['POST'])
def order4_dessert():
    if request.method == 'POST':
        orderid = request.form['orderid']
        budget = request.form['budget']
        spent =  request.form['spent']
        dessert_type = request.form['dessert_type']
        dessert_size = request.form['dessert_size']
        number_of_desserts = request.form['number_of_desserts']
        
        if dessert_type == "Soft ice":
            price = 20
        elif dessert_type == "Milkshake":
            price = 25
        elif dessert_type == "Pancake stack":
            price = 30
        elif dessert_type == "Waffles":
            price = 35

        # Determine price based on size and type
        if dessert_size == "Small":
            price = 1*int(price)
        elif dessert_size == "Medium": 
            price = 1.5 * int(price)
        elif dessert_size == "Large": 
            price = 2 * int(price)
        elif dessert_size == "Extra Large":
            price = 2.5 * int(price)
        price = int(number_of_desserts) * int(price)
        # insert into dessert and food table
        queries.insert_desserts(dessert_type, dessert_size, orderid, price, number_of_desserts)

        if request.form['action'] == 'next':
            spent = float(request.form['spent']) + float(price)
            # Fetch tuples from the database
            burgers = queries.select_burgers_from_order(orderid)
            beverages = queries.select_beverages_from_order(orderid)
            french_fries = queries.select_fries_from_order(orderid)
            desserts = queries.select_desserts_from_order(orderid)

            return render_template("order5_finish.html", burgers=burgers, beverages=beverages, 
                                   french_fries=french_fries, desserts=desserts, 
                                   orderid=orderid, budget=budget, spent=spent)
        
        elif request.form['action'] == 'extra_dessert':
            spent = float(request.form['spent']) + float(price)
            return render_template("order4_dessert.html", orderid=orderid, budget=budget, spent=spent)
        elif request.form['action'] == 'back':
            return render_template("order3_french_fries.html", orderid=orderid, budget=budget, spent=spent)   


@app.route("/order5_finish", methods=['GET', 'POST'])
def order5_finish():
    cursor = conn.cursor()
    orderid = request.form['orderid']
    budget = request.form['budget']
    spent =  request.form['spent'] 
    
    if request.method == 'POST':
        # Handle deletion of selected tuple
        delete_type = request.form['delete_type']
        delete_id = request.form['delete_id']
        if delete_type == 'burger':
            cursor.execute('''SELECT price FROM Food WHERE id = %s''', (delete_id,))
            value = cursor.fetchone()[0] 
            spent = float(spent) - float(value)
            cursor.execute('''DELETE FROM Food WHERE id = %s''', (delete_id,))

        elif delete_type == 'beverage':
            cursor.execute('''SELECT price FROM Food WHERE id = %s''', (delete_id,))
            value = cursor.fetchone()[0] 
            spent = float(spent) - float(value)
            cursor.execute('''DELETE FROM Food WHERE id = %s''', (delete_id,))

        elif delete_type == 'french_fries':
            cursor.execute('''SELECT price FROM Food WHERE id  = %s''', (delete_id,))
            value = cursor.fetchone()[0] 
            spent = float(spent) - float(value)
            cursor.execute('''DELETE FROM Food WHERE id = %s''', (delete_id,))

        elif delete_type == 'dessert':
            cursor.execute('''SELECT price FROM Food WHERE id  = %s''', (delete_id,))
            value = cursor.fetchone()[0] 
            spent = float(spent) - float(value)
            cursor.execute('''DELETE FROM Food WHERE id = %s''', (delete_id,))

        # Fetch tuples from the database
        conn.commit()
        burgers = queries.select_burgers_from_order(orderid)
        beverages = queries.select_beverages_from_order(orderid)
        french_fries = queries.select_fries_from_order(orderid)
        desserts = queries.select_desserts_from_order(orderid)
        
        if spent == 0:
            # Hvis alt er slettet
            return render_template("order_finish_options.html", orderid=orderid, spent=spent)

        else:
            return render_template("order5_finish.html", burgers=burgers, beverages=beverages, 
                                   french_fries=french_fries, desserts=desserts, 
                                   orderid=orderid, budget=budget, spent=spent)


    return render_template("order5_finish.html", burgers=burgers, beverages=beverages, 
                           french_fries=french_fries, desserts=desserts, 
                           orderid=orderid, budget=budget, spent=spent)


@app.route("/order_finish_options", methods=['GET'])
def order_finish_options():

    userid = session['userid']
    orderid = session['orderid']
    spent = request.args.get('spent')

    cur = conn.cursor()
    cur.execute('''UPDATE Users SET budget = budget - %s WHERE userid = %s''', (spent,userid,)) 
    cur.execute('''SELECT budget FROM Users WHERE userid = %s''', (userid,))
    conn.commit()

    return render_template("order_finish_options.html", orderid=orderid, spent=spent)

@app.route("/restart", methods=['POST'])
def restart():
    session.clear()
    return render_template("frame.html")

@app.route("/complaint", methods=['GET'])
def complaint():
    orderid = session.get('orderid')
    return render_template("complaint.html", orderid=orderid)


@app.route("/submit_complaint", methods=['POST'])
def submit_complaint():
    orderid = request.form['orderid']
    complaint_text = request.form['complaint_text']

    # Search for an 8-digit number in the complaint text
    phone_number_match = re.search(r'\b\d{8}\b', complaint_text)
    phone_number = phone_number_match.group() if phone_number_match else None
    # Insert into complaint table 
    queries.insert_complaint(orderid, phone_number, complaint_text)

    session.clear()
    return render_template("frame.html")

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)




