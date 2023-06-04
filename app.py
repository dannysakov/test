from flask import Flask, render_template, request, redirect
import sqlite3
import datetime


app = Flask(__name__)


connection = sqlite3.connect('library.db')
cursor = connection.cursor()

                         # -------  טבלת ספרים   --------
cursor.execute('CREATE TABLE IF NOT EXISTS Books (Id INTEGER PRIMARY KEY, Name TEXT, Author TEXT, YearPublished INTEGER, Type INTEGER)')

                         # -------  טבלת לקוחות   --------
cursor.execute('CREATE TABLE IF NOT EXISTS Customers (Id INTEGER PRIMARY KEY, Name TEXT, City TEXT, Age INTEGER)')

                         # --------  טבלת השאלות  ---------
cursor.execute('CREATE TABLE IF NOT EXISTS Loans (CustID INTEGER, BookID INTEGER, LoanDate TEXT, ReturnDate TEXT, ActualReturnDate TEXT)')

connection.commit()
connection.close()

class Loan:
    def __init__(self, customer_id, book_id, loan_date, return_date):
        self.customer_id = customer_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date

    def save(self):
        connection = sqlite3.connect('library.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Loans (CustID, BookID, LoanDate, ReturnDate) VALUES (?, ?, ?, ?)',
                       (self.customer_id, self.book_id, self.loan_date, self.return_date))
        connection.commit()
        connection.close()


#          _________________________   מסך הבית ____________________________


@app.route('/')
def index():
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    connection.close()
    return render_template('1_home.html', books=books)


#          _________________________  הוספת ספר ____________________________

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        year_published = request.form['year_published']
        book_type = request.form['book_type']

        connection = sqlite3.connect('library.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Books (Name, Author, YearPublished, Type) VALUES (?, ?, ?, ?)',
                       (name, author, year_published, book_type))
        connection.commit()
        connection.close()
        
        return render_template('2_add_book.html', book_added=True )

    return render_template('2_add_book.html')

#          _________________________   הוספת לקוח ____________________________


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        age = request.form['age']

        connection = sqlite3.connect('library.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Customers (Name, City, Age) VALUES (?, ?, ?)',
                       (name, city, age))
        connection.commit()
        connection.close()

       
        return render_template('3_add_customer.html', customer_added=True )

    return render_template('3_add_customer.html')


#          _________________________    השאלת ספר ____________________________


@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        book_id = request.form['book_id']
        loan_date = request.form['loan_date']
        loan_duration = request.form['loan_duration']

        return_date = datetime.datetime.strptime(loan_date, '%Y-%m-%d') + datetime.timedelta(days=int(loan_duration))
        return_date = return_date.strftime('%Y-%m-%d')

        connection = sqlite3.connect('library.db')
        cursor = connection.cursor()

                            # בדיקה עם הספר כבר הושאל
        cursor.execute('SELECT * FROM Loans WHERE BookID = ? AND ActualReturnDate IS NULL', (book_id,))
        existing_loan = cursor.fetchone()

        if existing_loan:
            error_message = "This book is already borrowed and has not been returned yet."
            Refresh = "Refresh the page and try to choose a different book"
            return render_template('3_borrow_book.html', error_message=error_message, Refresh=Refresh )

        loan = Loan(customer_id, book_id, loan_date, return_date)
        loan.save()

        return redirect('/loans')

    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    cursor.execute('SELECT Loans.*, Customers.Name, Books.Name FROM Loans INNER JOIN Customers ON Loans.CustID = Customers.Id INNER JOIN Books ON Loans.BookID = Books.Id')
    loans = cursor.fetchall()
    connection.close()

    return render_template('3_borrow_book.html', customers=customers, books=books, loans=loans)


#          _________________________   החזרת ספרים  ____________________________

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        customer_id = int(request.form['customer_id'])
        book_id = int(request.form['book_id'])
        return_date = request.form['return_date']

        connection = sqlite3.connect('library.db')
        cursor = connection.cursor()

                            # בדיקה אם הספר הוחזר בזמן
        cursor.execute('SELECT * FROM Loans WHERE CustID = ? AND BookID = ? AND ReturnDate >= ?',
                       (customer_id, book_id, return_date))
        existing_loan = cursor.fetchone()

        if not existing_loan:
            error_message = "The book was not returned on time. Or the book was not requested by the customer. You can go to the loan table to see the exact information "
            not_done = "The code is not yet finished to return the book just refresh the page and return it on time (in the future a button will be added that returns the book despite the delay)"
            return render_template('4_return_book.html', error_message=error_message,not_done=not_done)

        cursor.execute('DELETE FROM Loans WHERE CustID = ? AND BookID = ?',
                       (customer_id, book_id))

        connection.commit()
        connection.close()

        return redirect('/loans')

    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    connection.close()

    return render_template('4_return_book.html', customers=customers, books=books)


#          _________________________   כול הלקוחות  ____________________________


@app.route('/customers')
def view_customers():
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    connection.close()
    return render_template('5_customers.html', customers=customers)


#          _________________________   כול הספרים  ____________________________


@app.route('/books')
def view_books():
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    connection.close()
    return render_template('6_books.html', books=books)


#          _________________________   מחיקת לקוחות   ____________________________

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    if request.method == 'POST':
        customer_id = request.form['customer_id']

        connection = sqlite3.connect('library.db')
        cursor = connection.cursor()

                              # בדיקה אם ללקוח יש השאלות פתוחות
        cursor.execute('SELECT * FROM Loans WHERE CustID = ? AND ActualReturnDate IS NULL', (customer_id,))
        existing_loan = cursor.fetchone()

        if existing_loan:
            error_message = "Cannot delete the customer. There are open loans associated with the customer."
            Refresh ="Refresh the page and double check that the customer has indeed returned the book"
            return render_template('5_customers.html', error_message=error_message,Refresh=Refresh)
            
                                 # של הלקוח ביצוע המחיקה
        cursor.execute('DELETE FROM Customers WHERE Id = ?', (customer_id,))
        connection.commit()
        connection.close()

        return redirect('/customers')

    return render_template('5_customers.html')


#          _________________________   מחיקת ספרים   ____________________________


@app.route('/delete_book', methods=['POST'])
def delete_book():
    if request.method == 'POST':
        book_id = request.form['book_id']

        connection = sqlite3.connect('library.db')
        cursor = connection.cursor()
        

                             # בדיקה אם הספר מושאל
        cursor.execute('SELECT * FROM Loans WHERE bookID = ? AND ActualReturnDate IS NULL', (book_id,))
        existing_loan = cursor.fetchone()

        if existing_loan:
            error_message = "Cannot delete the book. There are open loans associated with the book."
            Refresh="Refresh the page and check again that the book has indeed been returned"
            return render_template('6_books.html', error_message=error_message,Refresh=Refresh)
                 
                               # ביצוע המחיקה של הספר
        cursor.execute('DELETE FROM Books WHERE Id = ?', (book_id,))
        connection.commit()
        connection.close()

        return redirect('/books')

    return render_template('6_books.html')


#          _________________________  כול ההשאלות ____________________________


@app.route('/loans')
def loans():
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Loans.*, Customers.Name, Books.Name FROM Loans INNER JOIN Customers ON Loans.CustID = Customers.Id INNER JOIN Books ON Loans.BookID = Books.Id')
    loans = cursor.fetchall()
    connection.close()
    return render_template('7_loans.html', loans=loans)


#          _________________________    חיפוש   ____________________________

@app.route('/Search', methods=['GET', 'POST'])
def Search():
    if request.method == 'POST':
        if 'customer_name' in request.form:
            name = request.form['customer_name']

            connection = sqlite3.connect('library.db')
            cursor = connection.cursor()

                                   # מידע על הלקוח
            cursor.execute('SELECT * FROM Customers WHERE Name = ?', (name,))
            customer = cursor.fetchone()

            if customer:
                                   # מידע על הספרים של אותו לקוח במידה ויש
                cursor.execute('SELECT Books.*, Loans.LoanDate, Loans.ReturnDate '
                               'FROM Books '
                               'INNER JOIN Loans ON Books.Id = Loans.BookID '
                               'INNER JOIN Customers ON Loans.CustID = Customers.Id '
                               'WHERE Customers.Name = ?', (name,))
                books = cursor.fetchall()

                connection.close()

                if books:
                    return render_template('8_Search.html', customer=customer, books=books)
                else:
                    error_message = "No books found for the customer."
                    return render_template('8_Search.html', customer=customer, error_message=error_message)
            else:
                error_message = "Customer not found (Make sure there are no unnecessary spaces in the search)."
                return render_template('8_Search.html', error_message=error_message)

        elif 'book_Name' in request.form:
            name = request.form['book_Name']

            connection = sqlite3.connect('library.db')
            cursor = connection.cursor()

                               # מידע על הספר
            cursor.execute('SELECT * FROM Books WHERE Name = ?', (name,))
            book = cursor.fetchone()

            if book:
                                 # מידע על לקוח שהשאיל את הספר במידה ויש

                cursor.execute('SELECT Customers.* '
                               'FROM Customers '
                               'INNER JOIN Loans ON Customers.Id = Loans.CustID '
                               'INNER JOIN Books ON Loans.BookID = Books.Id '
                               'WHERE Books.Name = ?', (name,))
                customers = cursor.fetchall()

                if customers:
                    connection.close()
                    return render_template('8_Search.html', book=book, customers=customers)
                else:
                    error_message = "No customers found for the book."
                    return render_template('8_Search.html', book=book, error_message=error_message)
            else:
                error_message = "Book not found (Make sure there are no unnecessary spaces in the search)."
                return render_template('8_Search.html', error_message=error_message)

    return render_template('8_Search.html')



#          _________________________  ההלואות שאוחרו  ____________________________


@app.route('/late_loans')
def late_loans():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()

                             # קבלת ההשאלות שאוחרו 
    cursor.execute('SELECT Loans.*, Customers.Name AS CustomerName, Books.Name AS BookName FROM Loans '
                   'INNER JOIN Customers ON Loans.CustID = Customers.Id '
                   'INNER JOIN Books ON Loans.BookID = Books.Id '
                   'WHERE ActualReturnDate IS NULL AND ReturnDate < ?', (current_date,))
    late_loans = cursor.fetchall()

    connection.close()


    return render_template('9_late_loans.html', late_loans=late_loans)



if __name__ == '__main__':
    app.run(debug=True)

