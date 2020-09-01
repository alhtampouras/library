from flask import render_template,url_for,flash,redirect,request
from library import app
from library.forms import *
from flask_login import current_user
import sqlite3




@app.route("/", methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('library/library.db')
        db = conn.cursor()
        
        emps = db.execute('''SELECT username from emp''').fetchall()
        members = db.execute('''SELECT username from emp''').fetchall()
        print(emps[0])
        if form.username.data in [x[0] for x in emps]:
            user = db.execute("SELECT * from emp where username='{}'".format(form.username.data)).fetchone()[0]
            password = db.execute("SELECT password from emp where username='{}'".format(form.username.data)).fetchone()[0]
            id = db.execute('''SELECT id from emp where username="{}"'''.format(form.username.data)).fetchone()[0]
        else:
            user = db.execute("SELECT * from member where username='{}'".format(form.username.data)).fetchone()[0]
            password = db.execute("SELECT password from member where username='{}'".format(form.username.data)).fetchone()[0]
            id = db.execute('''SELECT id from member where username="{}"'''.format(form.username.data)).fetchone()[0]
                                
        conn.close()
        
        if  user and password == form.password.data:
            if form.username.data == 'admin': 
                return redirect(url_for('admin'))
            elif form.username.data in [x[0] for x in emps]:
                return redirect(url_for('emp',emp=id))
            else:
                return redirect(url_for('member',member=id))
        
        else:
            flash(f'Login unsuccessfull','danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    form = RegisterationForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('library/library.db')
        db = conn.cursor()
        db.execute('''
            INSERT into member(first_name,last_name,b_day,address,town,postal_code,username,password) 
            values('{}','{}','{}','{}','{}',{},'{}','{}')'''.format(form.first_name.data,
                                                                    form.last_name.data,
                                                                    form.b_day.data,
                                                                    form.address.data,
                                                                    form.town.data,
                                                                    form.postal_code.data,
                                                                    form.username.data,
                                                                    form.password.data))
        
        flash(f'Your account has been created!','success')
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('sign_up.html', title='Sign Up', form=form)

@app.route("/admin", methods=['GET', 'POST'])

def admin():
    conn = sqlite3.connect('library/library.db')
    db = conn.cursor()
    member_form     = Member_form()
    book_form       = Book_form()
    emp_form        = Emp_form()
    publisher_form  = Publisher_form()
    
    all_emps        = db.execute('SELECT * from emp order by id').fetchall()
    all_members     = db.execute('SELECT * from member order by id ').fetchall()
    all_books       = db.execute('SELECT * from books order by id ').fetchall()
    all_pbs         = db.execute('SELECT * from publishers order by id ').fetchall()
    
    
    
    member_form.members.choices         = [(j,i) for j,i in zip(range(1,len(all_members)+1),all_members)]
    emp_form.emps.choices               = [(j,i) for j,i in zip(range(1,len(all_emps)+1),all_emps)]
    book_form.books.choices             = [(j,i) for j,i in zip(range(1,len(all_books)+1),all_books)]
    publisher_form.publishers.choices   = [(j,i) for j,i in zip(range(1,len(all_pbs)+1),all_pbs)]
    if request.method == 'POST':
        if request.form.get('remove_member'):
            db.execute('DELETE from member where id={}'.format(member_form.members.data))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))
        elif request.form.get('remove_emp'):
            db.execute('DELETE from Emp where id={}'.format(emp_form.emps.data))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))
        elif request.form.get('remove_book'):
            db.execute('DELETE from Books where id={}'.format(book_form.books.data))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))
        elif request.form.get('remove_publisher'):
            db.execute('DELETE from Publishers where id={}'.format(publisher_form.publishers.data))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))

        elif request.form.get('update_member'):
            conn.close()
            return redirect(url_for('member_update',member=member_form.members.data))
        elif request.form.get('update_emp'):
            conn.close()
            return redirect(url_for('emp_update',emp=emp_form.emps.data))
        elif request.form.get('update_book'):
            conn.close()
            return redirect(url_for('book_update',books=book_form.books.data))
        elif request.form.get('update_publisher'):
            conn.close()
            return redirect(url_for('publisher_update',publisher=publisher_form.publishers.data))

        elif request.form.get('add_emp'):
            return redirect(url_for('add_emp'))
        elif request.form.get('add_book'):
            return redirect(url_for('add_book'))
        elif request.form.get('add_publisher'):
            return redirect(url_for('add_publisher'))
    conn.close()  
    return render_template('admin.html', member_form=member_form,book_form=book_form,emp_form=emp_form,publisher_form=publisher_form )

@app.route("/member", methods=['GET', 'POST'])
def member():
    conn = sqlite3.connect('library/library.db')
    db = conn.cursor()
    id = request.args['member']
    
    
    book_form       = Book_form()
    all_books       = db.execute('SELECT * from books').fetchall()
        
    
    
    borrowed_books = db.execute('''SELECT id,title,year,page_cnt,publisher_id,number_of_copies from books as b
                                            join (select c.book_id from copies as c
                                                    join( select copy_id from borrow 
                                                        where member_id = {} and return_date is null)as br 
                                                    where c.id = br.copy_id) as f
                                            where b.id = f.book_id;'''.format(id)).fetchall() 
    
    book_form.borrowed_books.choices = [(i[0],i) for i in borrowed_books]
    available_books = [x for x in all_books if x not in borrowed_books]
    book_form.books.choices = [(i[0],i) for i in available_books]
    
    if request.method == 'POST':
        if request.form.get('borrow_book'):
            
            copy_id = db.execute('''SELECT id from copies where book_id={}'''.format(book_form.books.data)).fetchone()[0]
            db.execute('INSERT into borrow(member_id,copy_id) values ({},{});'.format(int(id),int(copy_id)))
            conn.commit()
            conn.close()
            
            return redirect(url_for('member',member=id))
        elif request.form.get('return_book'):
            
            db.execute('''UPDATE borrow set return_date=date("now") where member_id={} and 
                copy_id=(SELECT id from copies where book_id={})'''.format(id,book_form.borrowed_books.data))
            conn.commit()
            conn.close()
            return redirect(url_for('member',member=id))
      
    conn.close()  
    return render_template('member.html', book_form=book_form)

@app.route("/emp", methods=['GET', 'POST'])
def emp():
    conn = sqlite3.connect('library/library.db')
    db = conn.cursor()
    id = request.args['emp']
    form     = Member_form()
    all_members     = db.execute('SELECT * from member order by id ').fetchall()
    form.members.choices         = [(j,i) for j,i in zip(range(1,len(all_members)+1),all_members)]
    
    if request.method == 'POST':
        if request.form.get('send_reminder'):
            db.execute('INSERT into reminder(emp_id,member_id,date) values({},{},date("now"))'.format(id,form.members.data))
            conn.commit()
            conn.close()
            return redirect(url_for('emp',emp=id))
        
    conn.close()  
    return render_template('emp.html', form=form)

@app.route("/member_update", methods=['GET', 'POST'])

def member_update():
    conn = sqlite3.connect('library/library.db')
    db = conn.cursor()
    id = request.args['member']
    member = db.execute('SELECT * from member where id={}'.format(id)).fetchone()
    
    print(member)
    form = RegisterationForm()
    if request.form.get('submit'):
        db.execute('''UPDATE member SET 
            first_name="{}",last_name="{}",b_day="{}",address="{}",town="{}",postal_code={} 
            where id={}'''.format(form.first_name.data,
                                form.last_name.data,
                                form.b_day.data,
                                form.address.data,
                                form.town.data,
                                form.postal_code.data,
                                id))
        conn.commit()
        conn.close()
        flash(f'member successfully updated!','success')
        return redirect(url_for('admin'))

    conn.close()
    return render_template('member_update.html', title='member Update', form=form, member=member)

@app.route("/book_update", methods=['GET', 'POST'])

def book_update():
    conn = sqlite3.connect('library/library.db')
    db = conn.cursor()
    id = request.args['books']
    book = db.execute('SELECT * from books where id={}'.format(id)).fetchone()
    
    form = BookRegisterationForm()
    pb  = db.execute('SELECT name from publishers where id={}'.format(book[4])).fetchone()[0]
    
    if request.form.get('submit'):
        publisher_id = db.execute('''
            SELECT id from publishers where name="{}"'''.format(form.publisher.data)).fetchone()[0]
        
        db.execute('''UPDATE books SET 
            title="{}",year={},page_cnt={},publisher_id={},number_of_copies={} 
            where id={}'''.format(form.title.data,
                                form.year.data,
                                form.page_cnt.data,
                                publisher_id,
                                form.number_of_copies.data,
                                id))
        conn.commit()
        conn.close()
        flash(f'Book successfully updated!','success')
        return redirect(url_for('admin'))
    conn.close()
    return render_template('book_update.html', title='Book Update', form=form, book=book, pb=pb)

@app.route("/publisher_update", methods=['GET', 'POST'])

def publisher_update():
    conn = sqlite3.connect('library/library.db')
    db = conn.cursor()
    id = request.args['publisher']
    pb = db.execute('SELECT * from publishers where id={}'.format(id)).fetchone()
    
    form = Publisher_form()
    if request.form.get('update_publisher'):
        db.execute('UPDATE publishers SET name="{}",year={} where id={}'.format(form.name.data,form.year.data,id))
        flash(f'Publisher successfully updated!','success')
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))
    conn.close()
    return render_template('publisher_update.html', title='Publisher Update', form=form, pb=pb)

@app.route("/emp_update", methods=['GET', 'POST'])

def emp_update():
    conn = sqlite3.connect('library/library.db')
    db = conn.cursor()
    id = request.args['emp']
    emp = db.execute('SELECT * from Emp where id={}'.format(id)).fetchone()
    print(emp)
    form = EmpRegisterationForm()
    if request.form.get('submit'):
        
        if form.perm_temp.data == 'temp':
            perm_temp = {'perm':0,'temp':1,'perm_date':'','temp_num':form.temp_number.data}
        elif form.perm_temp.data == 'perm':
            perm_temp = {'perm':1,'temp':0,'perm_date':form.perm_date.data,'temp_num':0}
        else:
            flash(f'Incomplete form','danger')
            return redirect(url_for('emp_update',emp=id))
        db.execute('UPDATE Emp SET first_name="{}",last_name="{}",salary={},perm="{}",temp="{}",perm_date="{}",temp_number={} where id={}'.format(form.first_name.data,form.last_name.data,form.salary.data,perm_temp['perm'],perm_temp['temp'],perm_temp['perm_date'],perm_temp['temp_num'],id))
        conn.commit()
        conn.close()
        flash(f'Emploee successfully updated!','success')
        return redirect(url_for('admin'))
    conn.close()
    return render_template('emp_update.html', title='Emploee Update', form=form, emp=emp)

@app.route("/add_emp", methods=['GET', 'POST'])

def add_emp():
    conn = sqlite3.connect('library/library.db')
    db = conn.cursor()
    form = EmpRegisterationForm()
    if request.form.get('submit'):
        if form.perm_temp.data == 'temp':
            perm_temp = {'perm':0,'temp':1,'perm_date':'','temp_num':form.temp_number.data}
        elif form.perm_temp.data == 'perm':
            perm_temp = {'perm':1,'temp':0,'perm_date':form.perm_date.data,'temp_num':0}
        else:
            flash(f'Incomplete form','danger')
            return redirect(url_for('add_emp'))
    
        db.execute('''INSERT into emp(first_name,last_name,salary,perm,temp,perm_date,temp_number,username,password) 
                                values ('{}','{}',{},'{}','{}','{}',{},'{}','{}')'''.format(form.first_name.data,
                                                                            form.last_name.data,
                                                                            form.salary.data,
                                                                            perm_temp['perm'],
                                                                            perm_temp['temp'],
                                                                            perm_temp['perm_date'],
                                                                            perm_temp['temp_num'],
                                                                            form.username.data,
                                                                            form.password.data))
        conn.commit()
        conn.close()
        flash(f'Emploee Added','success')
        return redirect(url_for('admin'))
    
    conn.close()
    return render_template('add_emp.html', title='Add Emploee', form=form)

@app.route("/add_book", methods=['GET', 'POST'])

def add_book():
    conn = sqlite3.connect('library/library.db')
    db = conn.cursor()
    all_pbs         = db.execute('SELECT * from publishers order by id ').fetchall()
    
    form = BookRegisterationForm()
    form.publishers.choices   = [(j,i) for j,i in zip(range(1,len(all_pbs)+1),all_pbs)]
    if request.form.get('submit'):
        db.execute('''INSERT into books(title,year,page_cnt,publisher_id,number_of_copies) 
                values ('{}',{},{},{},{})'''.format(form.title.data,
                                                    form.year.data,
                                                    form.page_cnt.data,
                                                    form.publishers.data,
                                                    form.number_of_copies.data))
        conn.commit()
        conn.close()
        flash(f'Book Added','success')
        return redirect(url_for('admin'))
    
    conn.close()
    return render_template('add_book.html', title='Add Book', form=form)

@app.route("/add_publisher", methods=['GET', 'POST'])

def add_publisher():
    conn = sqlite3.connect('library/library.db')
    db = conn.cursor()
        
    form = PublisherRegisterationForm()
    
    if request.form.get('submit'):
        db.execute('''INSERT into publishers(name,year) 
                values ('{}',{})'''.format(form.name.data,form.year.data,))
        conn.commit()
        conn.close()
        flash(f'Publisher Added','success')
        return redirect(url_for('admin'))
    
    conn.close()
    return render_template('add_publisher.html', title='Add Publisher', form=form)
@app.route('/logout')
def logout():
    
    return redirect(url_for('login'))

# @app.route("/member", methods=['GET', 'POST'])
# @login_required
# def member():
#     form = admin_form()
#     form.members.choices = []
#     return render_template('member.html', form=form)

# @app.route("/test", methods=['GET', 'POST'])
# def test():
#     form = admin_form()
#     return render_template('member.html', form=form)

