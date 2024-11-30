*LIBRARY MANAGEMENT SYSTEM*
Video Demo:  https://youtu.be/kiakQULeKOs?si=s8LCmAWr2csP5oJc

DESCRIPTION
This Library System is a Python-based program specifically designed to handle core library operations efficiently. The system's primary functions include managing books, users, borrowing, 
and returning transactions. It ensures that all critical data, such as books, user details, and transaction records, are persistently stored using CSV files.

STUDENT ACCESS

      BROWSE BOOKS
          View the library's inventory with details such as Book ID, Title, Author, Published Year, and availability.
      
      REGISTER AS A USER
          If it's a student's first time borrowing, they must register by providing their name and section.
          Registered details are saved for future transactions.
    
      BORROW BOOKS
          Select a book using its Book ID.
          Specify a return date for the borrowed book.
          Borrowing actions are logged for accountability.
    
      RETURN BOOKS
          Confirm the borrowed book using its Book ID.
          The system updates the inventory to reflect the book's availability and adds remarks based on the return status.
    
      BORROWING AND RETURNING HISTORY
          Every borrowing and returning action is logged with the Username, Book ID, Borrow Date, Return Date, and Remarks.

LIBRARIAN MANAGEMENT

       VIEW BOOKS
         Access the complete list of books, including Book ID, Title, Author, Published Year
   
       ADD BOOKS
          Expand the library’s collection by providing Book ID, Title, Author, and Published Year.
          Newly added books are immediately available in the library’s inventory.
   
       DELETED BOOKS
          Remove books by searching for their Book ID and confirming the deletion.
          Deleted books are permanently removed from the system.
   
       REGISTER USER
          Register students by collecting their Username and Section.
          Skip registration if the student is already in the system.
   
      VIEW REGISTERED USER
          Access a list of all registered students with their names and sections.
   
      VIEW TRANSACTION HISTORY
          Monitor all borrowing and returning activities, including Username, Book ID, Borrow Date, Return Date, and Remarks
