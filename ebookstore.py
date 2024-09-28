import os
import sqlite3

# This is to ensure the correct working directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# Connect to the SQLite database (or create it if it doesn't exist)
db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()

# Create the book table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    qty INTEGER NOT NULL
)
''')

# Populate the table with initial data (if it's empty)
books = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
]

cursor.executemany('''
INSERT OR IGNORE INTO book (id, title, author, qty) VALUES (?, ?, ?, ?)
''', books)

db.commit()

# Function to display the menu options
def display_menu():
    print("\nBookstore Management")
    print("1. Enter new book")
    print("2. Update book details")
    print("3. Delete a book")
    print("4. Search for books")
    print("0. Exit")

# Function to enter a new book into the database
def enter_book():
    try:
        # Prompt user for book details
        id = int(input("Enter book ID: "))
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        qty = int(input("Enter quantity: "))
        
        # Insert the new book into the database
        cursor.execute('''
        INSERT INTO book (id, title, author, qty) VALUES (?, ?, ?, ?)
        ''', (id, title, author, qty))
        
        # Commit changes to the database
        db.commit()
        print("Book added successfully!")
    
    # Handle SQLite errors
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    # Handle value errors, such as entering non-integer values for ID or quantity
    except ValueError as ve:
        print(f"ValueError: {ve}")
    
    # Handle any other unexpected errors
    except Exception as ex:
        print(f"Unexpected error: {ex}")

# Function to update details of an existing book in the database
def update_book():
    try:
        # Prompt user to enter the ID of the book to update
        id = int(input("Enter book ID to update: "))
        
        # Prompt user for new details of the book (leave blank to keep unchanged)
        title = input("Enter new title (leave blank to keep unchanged): ")
        author = input("Enter new author (leave blank to keep unchanged): ")
        qty = input("Enter new quantity (leave blank to keep unchanged): ")

        # Check if the book ID exists in the database
        cursor.execute('SELECT COUNT(*) FROM book WHERE id = ?', (id,))
        if cursor.fetchone()[0] == 0:
            print("Book ID not found.")
            return

        # Update the title if a new title is provided
        if title:
            cursor.execute('''
            UPDATE book SET title = ? WHERE id = ?
            ''', (title, id))

        # Update the author if a new author is provided
        if author:
            cursor.execute('''
            UPDATE book SET author = ? WHERE id = ?
            ''', (author, id))

        # Update the quantity if a new quantity is provided
        if qty:
            cursor.execute('''
            UPDATE book SET qty = ? WHERE id = ?
            ''', (int(qty), id))

        # Commit the changes to the database
        db.commit()
        print("Book updated successfully!")
    
    # Handle SQLite errors
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    # Handle value errors, such as entering non-integer values for ID or quantity
    except ValueError as ve:
        print(f"ValueError: {ve}")
    
    # Handle any other unexpected errors
    except Exception as ex:
        print(f"Unexpected error: {ex}")

# Function to delete a book from the database
def delete_book():
    try:
        # Prompt user to enter the ID of the book to delete
        id = int(input("Enter book ID to delete: "))
        
        # Execute SQL command to delete the book from the database
        cursor.execute('''
        DELETE FROM book WHERE id = ?
        ''', (id,))
        
        # Commit the changes to the database
        db.commit()
        print("Book deleted successfully!")
    
    # Handle SQLite errors
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    # Handle value errors, such as entering non-integer values for ID
    except ValueError as ve:
        print(f"ValueError: {ve}")
    
    # Handle any other unexpected errors
    except Exception as ex:
        print(f"Unexpected error: {ex}")

# Function to search for books in the database by title or author
def search_books():
    try:
        # Displaying all books currently in the database
        print("\nAll books in the database:")
        cursor.execute('SELECT * FROM book')
        all_books = cursor.fetchall()
        
        # If there are books in the database, display them with headers
        if all_books:
            print(f"{'ID':<5} {'Title':<45} {'Author':<25} {'Qty':<5}")
            print("="*82)
            for book in all_books:
                print(f"{book[0]:<5} {book[1]:<45} {book[2]:<25} {book[3]:<5}")
        else:
            # If no books are found in the database
            print("No books found in the database.")

        # Prompt user to enter search term (title/author)
        search_term = input("\nEnter search term (title/author): ")
        
        # Search for books matching the search term in title or author fields
        cursor.execute('''
        SELECT * FROM book WHERE title LIKE ? OR author LIKE ?
        ''', ('%' + search_term + '%', '%' + search_term + '%'))
        
        # Fetch all matching results
        results = cursor.fetchall()

        # Display search results
        if results:
            for result in results:
                print(result)
        else:
            print("No books found.")
    
    # Handle SQLite errors
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    # Handle any other unexpected errors
    except Exception as ex:
        print(f"Unexpected error: {ex}")

# Main program loop to display menu and process user input
while True:
    display_menu()
    choice = input("Enter your choice: ")
    
    if choice == '1':
        enter_book()
    elif choice == '2':
        update_book()
    elif choice == '3':
        delete_book()
    elif choice == '4':
        search_books()
    elif choice == '0':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection when program ends
db.close()
