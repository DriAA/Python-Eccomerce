import mysql.connector
import random


# Initiate Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password"
)

# Initiate db.
mycursor = mydb.cursor(buffered=True)



# Create db.
mycursor.execute('DROP DATABASE IF EXISTS ecommerce')
mycursor.execute("CREATE DATABASE ecommerce")
mycursor.execute('USE ecommerce')



# Create Product
mycursor.execute("CREATE TABLE products(productID INT AUTO_INCREMENT PRIMARY KEY,url VARCHAR(255), product VARCHAR(255), gender VARCHAR(1), color VARCHAR(255), price INT, category VARCHAR(255) )")

# Create Inventory
mycursor.execute("CREATE TABLE inventory (inventoryID INT AUTO_INCREMENT,productID int,PRIMARY KEY (inventoryID),xs INT,sm INT, md INT, lg INT, xl INT, xxl INT,FOREIGN KEY (productID) REFERENCES products(productID))")




# Create User 
mycursor.execute("CREATE TABLE users (userID INT AUTO_INCREMENT, PRIMARY KEY (userID),email VARCHAR(255), username VARCHAR(255), password VARCHAR(255))")

# Create Cart
# CartID - UserID
mycursor.execute("CREATE TABLE carts (cartID INT AUTO_INCREMENT, PRIMARY KEY (cartID), userID INT, FOREIGN KEY (userID) REFERENCES users(userID))")

# Create Cart Items.
# ItemID -  CartID - ProductID - Quantity
mycursor.execute('CREATE TABLE cartItem (cartItemID INT AUTO_INCREMENT,PRIMARY KEY (cartItemID), cartID INT, productID INT, size VARCHAR(3), quantity INT, FOREIGN KEY (cartID) REFERENCES carts(cartID), FOREIGN KEY (productID) REFERENCES products(productID)) ')












# Create Womens DB
def generateWomens():
  womenProducts = "INSERT INTO products (product, url, gender, color, price, category) VALUES (%s, %s, %s, %s, %s, %s)"

  items = [
    ('Heels','https://images.unsplash.com/photo-1543163521-1bf539c55dd2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8cHJvZHVjdHxlbnwwfDJ8MHx8&auto=format&fit=crop&w=500&q=60', 'w', 'blue', random.randint(5,40),'shoes'),
    ('Glasses','https://images.unsplash.com/photo-1508296695146-257a814070b4?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MjR8fHByb2R1Y3R8ZW58MHwyfDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60','w' ,'pink', random.randint(5, 40), 'misc'),
    ('Watch','https://images.unsplash.com/photo-1562157646-4303261af91e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTAyfHxwcm9kdWN0fGVufDB8MnwwfHw%3D&auto=format&fit=crop&w=500&q=60','w','black', random.randint(5, 40), 'misc'),
    ('Lipstick','https://images.unsplash.com/photo-1614159102350-fc3c9eedead5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MjM0fHxwcm9kdWN0fGVufDB8MnwwfHw%3D&auto=format&fit=crop&w=500&q=60','w','pink', random.randint(5, 40), 'misc'),
    ('Gold Ring','https://images.unsplash.com/photo-1630918395670-afbb740fc57d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MjM5fHxwcm9kdWN0fGVufDB8MnwwfHw%3D&auto=format&fit=crop&w=500&q=60','w','gold',random.randint(40,100), 'misc'),
    ('Skincare', 'https://images.unsplash.com/photo-1596099832784-ffd0f966e8b8?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mjg4fHxwcm9kdWN0fGVufDB8MnwwfHw%3D&auto=format&fit=crop&w=500&q=60', 'w', 'red', random.randint(5,40), 'misc'),
    ('Silk Dress', 'https://images.unsplash.com/photo-1524041255072-7da0525d6b34?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8ZHJlc3N8ZW58MHwyfDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60','w', 'black', random.randint(5, 40), 'dress'),
    ("Perfume", 'https://images.unsplash.com/photo-1589820933732-5594c9d89076?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OHx8d29tZW4lMjBwcm9kdWN0fGVufDB8MnwwfHw%3D&auto=format&fit=crop&w=500&q=60', 'w' , 'gold', random.randint(12,40), 'perfume'),
    ('Purse', 'https://images.unsplash.com/photo-1591348278999-ee1d0c06ed7b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTB8fHdvbWVuJTIwcHJvZHVjdHxlbnwwfDJ8MHx8&auto=format&fit=crop&w=500&q=60', 'w','red', random.randint(50,125), 'purse')
  ]

  mycursor.executemany(womenProducts, items)

  mydb.commit()

  print(mycursor.rowcount, "was inserted for the womens Database.")

  womenInventory = 'INSERT INTO inventory (productID, xs, sm, md, lg, xl, xxl) VALUES (%s, %s, %s, %s, %s, %s, %s)'
  inventory = [
    (1, 5, 2, 9, 11, 7, 2),
    (2, 0, 11, 8, 1, 23, 2),
    (3, 10, 0, 1, 5, 1, 1),
    (4, 1, 11, 5, 15, 2, 3),
    (5, 25, 1, 14, 2, 4, 5),
    (6, 2, 0, 10, 8, 1, 12),
    (7, 12, 0, 1, 12, 15, 0),
    (8, 21, 0, 1, 3, 9, 14),
    (9, 7, 0, 12, 8, 11, 0)
  ]

  mycursor.executemany(womenInventory, inventory)

  mydb.commit()

  print(mycursor.rowcount, "was inserted for the women's inventory Database.")

generateWomens()



# Create Mens DB
def generateMens():
    
    # Add at least 25 Items 
    mensProducts = "INSERT INTO products (product, url, gender, color, price, category) VALUES (%s, %s, %s, %s, %s, %s)"

    items = [
        ('Glasses', 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8cHJvZHVjdHxlbnwwfDJ8MHx8&auto=format&fit=crop&w=500&q=60', 'm', 'gold', random.randint(5,40), 'misc'),
        ('Watch', 'https://images.unsplash.com/photo-1562157705-52df57a5883b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80', 'm', 'black',random.randint(5,40), 'misc'),
        ('Jean', 'https://images.unsplash.com/photo-1604176354204-9268737828e4?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8bWVuJTIwamVhbnN8ZW58MHwyfDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60','m','blue',random.randint(5,40), 'pants'),
        ('Shoes', 'https://images.unsplash.com/photo-1491553895911-0055eca6402d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cHJvZHVjdHxlbnwwfDJ8MHx8&auto=format&fit=crop&w=500&q=60','m','silver',random.randint(5,40),'shoes'),
        ('T-Shirt', 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8bWVuJTIwc2hpcnR8ZW58MHwyfDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60','m','white',random.randint(5,40),'shirt'),
        ('Jacket', 'https://images.unsplash.com/photo-1636016954413-44070ee44f8c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8N3x8bWVuJTIwcGFudHN8ZW58MHwyfDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60', 'm','blue',random.randint(5,40), 'jacket'),
        ('Sneakers', 'https://images.unsplash.com/photo-1605034313761-73ea4a0cfbf3?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTN8fHByb2R1Y3R8ZW58MHwyfDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60', 'm', 'grey',random.randint(5,40), 'shoes'),
        ('Knife', 'https://images.unsplash.com/photo-1612197622878-14dbe3ecc032?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NDl8fHByb2R1Y3R8ZW58MHwyfDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60','m','black',random.randint(5,40), 'misc'),
        ('Wallet', 'https://images.unsplash.com/photo-1601592996763-f05c9c80a7f1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8d2FsbGV0fGVufDB8MnwwfHw%3D&auto=format&fit=crop&w=500&q=60', 'm', 'black', random.randint(5,40),'misc')
    ]
    mycursor.executemany(mensProducts, items)

    mydb.commit()

    print(mycursor.rowcount, "was inserted for the mens Database.")


    mensInventory = 'INSERT INTO inventory (productID, xs, sm, md, lg, xl, xxl) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    inventory = [
      (10, 5, 2, 9, 11, 7, 2),
      (11, 0, 11, 8, 1, 23, 2),
      (12, 10, 0, 1, 5, 1, 1),
      (13, 1, 11, 5, 15, 2, 3),
      (14, 25, 1, 14, 2, 4, 5),
      (15, 2, 0, 10, 8, 1, 12),
      (16, 12, 0, 1, 12, 15, 0),
      (17, 21, 0, 1, 3, 9, 14),
      (18, 7, 0, 12, 8, 11, 0)
    ]


    mycursor.executemany(mensInventory, inventory)

    mydb.commit()

    print(mycursor.rowcount, "was inserted for the men's inventory Database.")
generateMens()
