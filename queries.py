from project import conn


def select_budget(userid):
    cursor = conn.cursor()
    sql = """
    SELECT budget 
    FROM users 
    WHERE userid= %s
    """
    cursor.execute(sql, (userid,))
    budget = None
    if cursor.rowcount:
        budget = cursor.fetchone()[0] 
    cursor.close()
    return budget

def select_userid(username):
    cursor = conn.cursor()
    sql = """
    SELECT userid 
    FROM users 
    WHERE username = %s
    """
    cursor.execute(sql, (username,))
    userid = cursor.fetchone()[0]
    cursor.close()
    return userid

def select_usernames():
    cursor = conn.cursor()
    sql = """
    SELECT username
    FROM users
    """
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    return users

def select_budgets_and_usernames():
    cursor = conn.cursor()
    sql = """
    SELECT username, budget 
    FROM users
    """
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    return users


def insert_order(userid):
    cursor = conn.cursor()
    sql = """
    INSERT INTO orders (customerid)
    VALUES (%s) returning orderid
    """
    orderid = None
    try:
        cursor.execute(sql,(userid,))
    except:
        conn.rollback()
    else: 
        conn.commit()
        orderid = cursor.fetchone()[0]
    finally:
        cursor.close()
    return orderid

def insert_user(username, budget):
    cursor = conn.cursor()
    sql = """
    INSERT INTO Users(username, budget) 
    VALUES (%s, %s)
    """
    try:
        cursor.execute(sql,(username, budget))
    except:
        conn.rollback()
        return 0
    else: 
        conn.commit()
    finally:
        cursor.close()
    return 1

def insert_burger(burger_type, patty_type, bun_type, orderid, price, amount):
    cursor = conn.cursor()
    sql = """
    INSERT INTO food (price, amount) 
    VALUES (%s, %s)
    """
    sql2 = """
    INSERT INTO Burgers (burger_type, patty_type, bun_type, orderid, food_id)
    values (%s, %s,%s,%s,(select max(id) from food));
    """
    try:
        cursor.execute(sql,(price, amount))
        cursor.execute(sql2,(burger_type, patty_type, bun_type, orderid))
    except:
        conn.rollback()
    else: 
        conn.commit()
    finally:
        cursor.close()

def insert_beverage(beverage_type, beverage_volume, orderid, price, amount):
    cursor = conn.cursor()
    sql = """
    INSERT INTO food (price, amount) 
    VALUES (%s, %s)
    """
    sql2 = """
    INSERT INTO Beverages (beverage_type, beverage_volume, orderid, food_id)
    values (%s, %s,%s, (select max(id) from food));
    """
    try:
        cursor.execute(sql,(price, amount))
        cursor.execute(sql2,(beverage_type, beverage_volume, orderid))
    except Exception as e:
        conn.rollback()
        print(e)
    else: 
        conn.commit()
    finally:
        cursor.close()

def insert_french_fries(french_fries_type, french_fries_size, orderid, price, amount):
    cursor = conn.cursor()
    sql = """
    INSERT INTO food (price, amount) 
    VALUES (%s, %s)
    """
    sql2 = """
    INSERT INTO French_fries(french_fries_type, french_fries_size, orderid, food_id)
    values (%s, %s,%s, (select max(id) from food));
    """
    try:
        cursor.execute(sql,(price, amount))
        cursor.execute(sql2,(french_fries_type, french_fries_size, orderid))
    except Exception as e:
        conn.rollback()
        print(e)
    else: 
        conn.commit()
    finally:
        cursor.close()

def insert_desserts(dessert_type, dessert_size, orderid, price, amount):
    cursor = conn.cursor()
    sql = """
    INSERT INTO food (price, amount) 
    VALUES (%s, %s)
    """
    sql2 = """
    INSERT INTO desserts (dessert_type, dessert_size , orderid, food_id)
    VALUES (%s, %s,%s, (select max(id) from food));
    """
    try:
        cursor.execute(sql,(price, amount))
        cursor.execute(sql2,(dessert_type, dessert_size, orderid))
    except Exception as e:
        conn.rollback()
        print(e)
    else: 
        conn.commit()
    finally:
        cursor.close()

def insert_complaint(orderid, phonenumber, complaint_text):
    cursor = conn.cursor()
    sql = """
    INSERT INTO Complaints (orderid, phonenumber, complaint_text) 
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(sql,(orderid, phonenumber, complaint_text))
    except Exception as e:
        conn.rollback()
        print(e)
    else: 
        conn.commit()
    finally:
        cursor.close()

def select_burgers_from_order(orderid):
    cursor = conn.cursor()
    sql = """
    select * from burgers
    inner join food on burgers.food_id=food.id
    where orderid = %s
    """
    cursor.execute(sql, (orderid,))
    burgers = cursor.fetchall()
    return burgers

def select_beverages_from_order(orderid):
    cursor = conn.cursor()
    sql = """
    select * from beverages
    inner join food on beverages.food_id=food.id
    where orderid = %s
    """
    cursor.execute(sql, (orderid,))
    beverages = cursor.fetchall()
    return beverages

def select_fries_from_order(orderid):
    cursor = conn.cursor()
    sql = """
    select * from french_fries
    inner join food on french_fries.food_id=food.id
    where orderid = %s
    """
    cursor.execute(sql, (orderid,))
    fries = cursor.fetchall()
    return fries

def select_desserts_from_order(orderid):
    cursor = conn.cursor()
    sql = """
    select * from desserts
    inner join food on desserts.food_id=food.id
    where orderid = %s
    """
    cursor.execute(sql, (orderid,))
    desserts = cursor.fetchall()
    return desserts





