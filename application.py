# importing libraries
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_mysqldb import MySQL

# creating flask application
app=Flask(__name__) 
app.secret_key='flash message'

# configuring database
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='monkey'
app.config['MYSQL_PASSWORD']='tail'
app.config['MYSQL_DB']='college'

mysql=MySQL(app)


# home page
@app.route("/")
def index():
    return render_template("index.html")

# login function
@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        cursor=mysql.connection.cursor()
        id_num=request.form['id_num']
        password=request.form['password']
        cursor.execute("SELECT * FROM faculty WHERE id_num=%s",(id_num,))
        data=cursor.fetchone()
        if(data):
            cursor.execute("SELECT num,id_num,from_date,to_date,reason FROM leave_application WHERE status='n'  ORDER BY num DESC")
            applications=cursor.fetchall()
            cursor.close()
            return render_template("index.html", faculty=[data], applications=applications)
        cursor.execute("SELECT * FROM student_details WHERE id_num=%s",(id_num,))
        data=cursor.fetchone()
        cursor.close()
        if(data[-1]==password):
            return render_template("index.html", student=[data])
        else:
            flash("Incorrect password!")
            return render_template("index.html", error="incorrect_login_password")

# registration function
@app.route("/register",methods=['POST'])
def register():
    if request.method=="POST":
        id_num=request.form['id_num']
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        password=request.form['password']
        conf_password=request.form['confirm_password']

        if(password!=conf_password):
            flash("Unmatched passwords!")
            return render_template("index.html", data=[id_num,name,email,phone,password],
                                   error="umatched_password1")
        cursor=mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO student_details VALUES (%s,%s,%s,%s,%s)",(id_num,name,email,phone,password))
        except Exception as e:
            flash(e)
        mysql.connection.commit()
        cursor.close()
        flash("Registration successful!")
        return redirect(url_for('index'))
    
# password reset function
@app.route("/reset", methods=['POST'])
def reset():
    if request.method=="POST":
        id_num=request.form['id_num']
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        password=request.form['password']
        conf_password=request.form['confirm_password']

        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM student_details WHERE id_num=%s and name=%s and email=%s and phone=%s",(id_num,name,email,phone))
        data=cursor.fetchone()
        if(data):
            cursor.execute('UPDATE student_details SET password=%s WHERE id_num=%s',(password,id_num))
            mysql.connection.commit()
            cursor.close()
            flash("Reset successful!")
            return render_template('index.html')
        else:
            flash("Unmatched details!")
            return render_template('index.html', error="unmatched")

# leave application function     
@app.route('/apply_leave', methods=['POST'])
def apply_leave():
    if request.method=='POST':
        id_num=request.form['id_num']
        from_date=request.form['from_date']
        to_date=request.form['to_date']
        reason=request.form['reason']

        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO leave_application(id_num,from_date,to_date,reason) VALUES (%s,%s,%s,%s)",(id_num,from_date,to_date,reason))
        mysql.connection.commit()
        flash("Applied successfully!")
        return render_template('index.html', student=[[id_num]])

# application dashboard function 
@app.route("/history", methods=['POST'])
def history():
    if request.method=='POST':
        id_num=request.form['id_num']
        
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM leave_application WHERE id_num=%s ORDER BY num DESC",(id_num,))
        data=cursor.fetchall()
        cursor.close()
        return render_template('index.html', student=[[id_num,'checked']], previous=data)
    
# application delete function
@app.route("/delete", methods=['POST'])
def delete():
    if request.method=='POST':
        num=request.form['num']
        id_num=request.form['id_num']

        cursor=mysql.connection.cursor()
        cursor.execute("DELETE FROM leave_application WHERE num=%s",(num,))
        mysql.connection.commit()
        flash("Deleted successfully!")

        cursor.execute("SELECT * FROM leave_application WHERE id_num=%s",(id_num,))
        data=cursor.fetchall()
        cursor.close()
        return render_template('index.html', student=[[id_num,'checked']], previous=data)

# leave grant function  
@app.route('/grant', methods=["POST"])
def grant():
    if request.method=='POST':
        fac_id_num=request.form['fac_id_num']
        id_num=request.form['id_num']

        cursor=mysql.connection.cursor()
        cursor.execute("UPDATE leave_application SET status='y' WHERE num=%s",(id_num,))
        mysql.connection.commit()
        flash("Leave granted!")
        
        cursor.execute("SELECT * FROM faculty WHERE id_num=%s",(fac_id_num,))
        data=cursor.fetchone()
        cursor.execute("SELECT num,id_num,from_date,to_date,reason FROM leave_application WHERE status='n'")
        applications=cursor.fetchall()
        cursor.close()
        return render_template("index.html", faculty=[data], applications=applications)

# leave deny function
@app.route("/deny", methods=["POST"])
def deny():
    if request.method=='POST':
        fac_id_num=request.form['fac_id_num']
        id_num=request.form['id_num']

        cursor=mysql.connection.cursor()
        cursor.execute("UPDATE leave_application SET status='r' WHERE num=%s",(id_num,))
        mysql.connection.commit()
        flash("Leave rejected!")
        
        cursor.execute("SELECT * FROM faculty WHERE id_num=%s",(fac_id_num,))
        data=cursor.fetchone()
        cursor.execute("SELECT num,id_num,from_date,to_date,reason FROM leave_application WHERE status='n'")
        applications=cursor.fetchall()
        cursor.close()
        return render_template("index.html", faculty=[data], applications=applications)

if __name__=="__main__":
    app.run(debug=True) # running the appplication