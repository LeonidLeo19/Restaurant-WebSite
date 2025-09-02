from flask import Flask, render_template,redirect,request, session
from db.database import Add_User, Check_User, Get_Available_Tables, Make_Tables, Get_id,\
    make_reservation,Get_All_Tables, Get_Available_Tables, Get_user_reservations, Cancel_Reservation
from datetime import datetime, date, timedelta
from datetime import datetime, timedelta
from flask import request, session, redirect, render_template

app = Flask(__name__)
app.secret_key='secret_key'

num_tables = 10
Make_Tables(num_tables)

@app.route('/')
def main():
    logged_in = session.get('logged_in', False)
    return render_template('main.html', logged_in=logged_in)

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reservation')
def reservation_today():
    if not session.get('logged_in'):
        return redirect('/login')

    today = date.today()
    min_date = today.isoformat()
    max_date = (today + timedelta(days=28)).isoformat()
    return render_template(
        'reservation.html',
        min_date=min_date,
        max_date=max_date
    )


@app.route('/reserve', methods=['POST'])
def reservation():
    day = request.form['reservation_date']

    if not session.get('logged_in'):
        return redirect('/login')

    free_tables=Get_Available_Tables(day)

    return render_template(
        'reserve.html',
        logged_in=True,
        day=day,
        free_tables=free_tables
    )



@app.route('/succsess', methods=['POST','GET'])
def succsess():
    user_id=Get_id(session['username'],session['password'])
    table_number=request.form.get('table_id')
    day=request.form.get('reservation_date')
    make_reservation(user_id,table_number,day)
    return render_template('sucсsess.html')
    
        

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if not Add_User(username, email, password):
            return render_template('registration.html', error='User already exists')
        session['logged_in'] = True
        session['username'] = username
        session['password'] = password
        return redirect('/')
    return render_template('registration.html')


@app.route('/check_user', methods=['POST'])
def check_user():
    username = request.form['username']
    password = request.form['password']
    if not Check_User(username, password):
        return render_template('login.html', error='Incorrect username or password!!!')
    else:
        session['logged_in'] = True
        session['username'] = username
        session['password'] = password
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

@app.route('/my_account')
def my_account():
    logged_in = session.get('logged_in', False)
    if not logged_in:
        return redirect('/login')
    user_reservations=Get_user_reservations(Get_id(session['username'],session['password']))
    return render_template('my_account.html',user_reservations=user_reservations)

@app.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    reservation_id=request.form.get('reservation_id')
    Cancel_Reservation(reservation_id)
    return redirect('/my_account')

if __name__=="__main__":
    app.run(debug=True)