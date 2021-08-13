from flask import Flask, render_template, request, jsonify,flash
import sqlite3 as sql
from flask import Flask, redirect, url_for



app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def Log():
    return render_template("login.html")

@app.route("/login", methods = ["GET","POST"])
def Login():
    l_id = request.form["logname"]
    l_pass  = request.form["logpass"]

    tab=l_id+l_pass
    #print("name")
    if request.method == 'POST':
        print("name")
        l_id = request.form["logname"]
        l_pass  = request.form["logpass"]

        tab=l_id+l_pass
        print(tab)
        return redirect(f"/add-details/{tab}")
    return render_template('index.html')

@app.route("/sign",methods=["GET","POST"])
def sign():
    return render_template("signup.html")

@app.route("/regis",methods=["GET","POST"])
def regis():
    u_id = request.values.get("signu_id")
    s_pass  = request.values.get("sign_pass")
    print(u_id)
    print(s_pass)
    table_name=u_id+s_pass
    print(table_name)
    try:
        conn=sql.connect('main.db')

        print("Opened database successfully")
        create="CREATE TABLE "+table_name+" (detail TEXT, cred TEXT)"
        conn.execute(create)
        #conn.execute("select * from credential")

        print("Table created successfully")
        conn.close()
        return render_template("success.html")
    except:
        return render_template("invalid.html", a="Username and password are already taken. Try another.")



@app.route("/add-details/<tab>",methods = ["GET","POST"])
def add_details(tab):
    #tab = request.form.get("tab")
    if request.method == 'GET':
        print(f"Your name is {tab}")
        try:
            con = sql.connect("main.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            a=f"select * from {tab}"
            print(a)
            cur.execute(a)
            return render_template('index.html',tab=tab) 
        except :
            return render_template('invalid.html',invalid='Please enter a valid data')
                
    
        
    if request.method == 'POST':
        detail = request.values.get("detail")
        credential  = request.values.get("credential")
        print(detail)
        with sql.connect("main.db") as con:
                cur = con.cursor()
                ins="INSERT INTO "+tab+f" (detail,cred) VALUES {(detail,credential)}"
                print(ins)
                cur.execute(str(ins))
                
                con.commit()
        return render_template("index.html",a="values added successfully",tab=tab)
        con.close()





@app.route("/list/<tab>",methods = ["GET","POST"])
def list_details(tab):

    #tab = request.form["tabname"]
    print(tab)
    con = sql.connect("main.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    a=f"select * from {tab}"
    print(a)
    cur.execute(a)

    rows = cur.fetchall()
    print(rows)
    for r in rows:
        print(r)
        
    return render_template("listdetail.html",rows = rows,tab=tab)
@app.route("/search/<tab>",methods = ["GET","POST"])
def search(tab):
    print(tab)
    return render_template("searchlist.html",tab=tab)
@app.route("/search-details/<tab>",methods = ["GET","POST"])
def search_details(tab):
    search_value = request.values.get("search")
    tab=tab
    print(search_value)
    con = sql.connect('main.db')
    con.row_factory = sql.Row
   
    cur = con.cursor()
    a=f"select * from {tab}"
    cur.execute(a)

    rows = cur.fetchall()
    print(rows)
    
    for r in rows:
        print(r)
        for s in r:
            print(s)
            if(search_value==s):
                print(search_value)
                a="SELECT cred FROM credential WHERE detail = "+search_value
                b=f'SELECT * FROM {tab} WHERE detail=?'
                cur.execute(b, (search_value,))
                sear = cur.fetchone()
                print(sear)
                for i in sear:
                    print(i)
                a=sear[1]
                print(a)
                return render_template("searchlist.html",a=a,sear=search_value)

            else:
                a="Not exists"
    return render_template("searchlist.html",a=a,tab=tab)



if __name__ == '__main__':
    app.run(port=5500,debug=True)