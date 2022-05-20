**Overview**
---
  _A simple app to view the list of books, add new book, edit an existing books and delete them. You can also import book from googleApi by author_
* **EndPoints**

  * _/books_ `GET`, `POST` - list of all books, adding new book if post
  * _/books/<book_id>_ `GET`, `PUT`, `PATCH`, `DELETE` - book of given id (book id match id from database)
  * _/books/authors_ `GET`, `POST` - list of all authors, adding new author if post
  * _/books/import_ `POST` - import data from googleApi and save to database, you can get here also with `GET` but technically its not supported

 
* **URL Params**

   _URL params are provided for `/books/` endpoint_

    * **all params are optional:**<br />
      * author=name - provide filtering over authors, can pass many params with author and response list witch all matching authors<br />
      * from=date&to=date - provide filtering over published date range<br />
      * acquired=true, or false - filter list by the acquired state (if the book is already acquired or not).<br />
      * title=title_of_book,- filter list by the title of the book.<br />
      * book_id=id_from_google_api,- filter list by the id of the book from googleApi.<br />


* **Data Params**

  _Method Post for endpoint /books/import require Data Param_
    * **Example of param body data:**  <br />
    `{ "author" : "Tolkien" }`

* _Link URL for working App:_ https://stxtaskbooks.herokuapp.com/books/ <br />
