import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits

    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password

def insert_user(user_name, password):
    sql = 'INSERT INTO user_sample VALUES(default, %s, %s, %s)'

    salt = get_salt()
    hashed_password = get_hash(password, salt)

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name, hashed_password, salt))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError :
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count

def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM user_sample WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name,))
        user = cursor.fetchone()

        if user != None:
            # SQLの結果からソルトを取得
            salt = user[1]

            # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
            hashed_password = get_hash(password, salt)

            # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password == user[0]:
                flg = True

    except psycopg2.DatabaseError :
        flg = False

    finally :
        cursor.close()
        connection.close()

    return flg

def select_all_books():
    connection=get_connection()
    cursor=connection.cursor()
    
    sql='SELECT id, ISBN, bookname, writer, shupansha FROM book'
    
    cursor.execute(sql)
    rows=cursor.fetchall()
    
    print(rows)
    cursor.close()
    connection.close()
    
    return rows

def search_book(bookname):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id,ISBN,bookname,writer,shupansha FROM book WHERE bookname LIKE %s'
    
    title_pattern = f'%{bookname}%'  # Add wildcard characters to the title pattern
    
    cursor.execute(sql, (title_pattern,))
    
    results = cursor.fetchall()
 
    cursor.close()
    connection.close()

    return results


def insert_book(isbn, bookname, writer, shupansha):
    connection = get_connection()
    cursor = connection.cursor()
    sql='INSERT INTO book VALUES (default, %s, %s, %s,%s)'
    
    cursor.execute(sql, (isbn, bookname, writer, shupansha))
    
    connection.commit()
    cursor.close()
    connection.close()
