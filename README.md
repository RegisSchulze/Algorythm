# Text summarization

- Type of challenge: Learning
- Duration: `1 week`
- Deadline : `07/05/2021 09:00 AM`
- Team challenge: Solo project

## Mission objectives

- Use of tokenization, stemming and lemmatization for exploration of text-based datasets.
- Explore state-of-the-art algorithms for text summarization.
- Use of transformers.
- Evaluate the performance of pre-trained models.
- Development and deployment of the dashboard for text summarization.

## The Mission

A book publishing company is interested in increasing its online sales. The marketing department discovered the way people read is evolving and now rather than reading the full book, people prefer to get an overview of the main ideas expressed by the author. The digital era also means that customers want to get answers not from one book but from thousands immediately.

You have the task of developing an "AI-powered tool" able to "read" the content of any given book and make a summarization of the text. Also, the tool has to be deployed online since the company is looking to integrate the program into their website and connect it with the database where the books are stored.


![(GIF)](https://media.giphy.com/media/MhAxhXZ0uEaer0U19j/giphy.gif)

### Must-have features

A minimum valuable product must include: 

- An online dashboard where the user can select or upload an e-book and the summary is automatically generated. 

You can decide the best strategy for improving the results. For example, summarizing by paragraph, by chapters, or by looking at the full book content.

### Nice to have features

- The users can also enter paragraphs of information to be summarized.
- The users can query questions to be answered according to the content of the book.
- The queries are answered according to the content of multiple books on the same or similar topics.
- Any other interesting application that you could develop using transformers


### Miscellaneous information

For developing purposes, you can work with the public-domain books from [Project Gutenberg](https://www.gutenberg.org/) a collection of more than 60K e-books.

- For a first exploration and testing of your code, you can explore a classical of Jule Verne:

[Around the World in Eighty Days by Jules Verne](https://www.gutenberg.org/ebooks/103)

- After, you can move forward and evaluate your program by exploring other books, you can limit your exploration to specific domains or topics.

The data is available in several formats such as HTML, UTF-8, feel free to work with the most convenient for your application.

### Constraints

- The dashboard should be easy to access and manipulate for any user without coding experience.
- Create **functions**, do **not** create a single huge script
- Each **function** has to be typed
- Your code should be **commented**
- Your code should be **cleaned of any commented unused code**.

## Deliverables

1. Publish your source code on the GitHub repository.
2. **Small presentation (10 minutes) about your findings**
3. Dashboard representative of data insights
4. Pimp up the README file:
   - Description
   - Installation
   - Usage
   - ⚠️**DATA SOURCES**
   - (Visuals)
   - (Contributors)
   - (Timeline)
   - (Personal situation)

## Evaluation criteria

### Technical

- Publish clean and readable code on Github.
- README has the format specified in the #Deliverables section
- Use of libraries for Natural Language Processing
- Data has been preprocessed (tokenization, lemmatization, etc..)
- Exploration of data using tokenization, stemming and lemmatization.
- Transformers were used for summarizing.
- Several pre-trained models were tested.
- The performance of the model was evaluated.
- Dashboard is user friendly without coding experience.
- The program works for any given book.

### Soft-skills

- Communication with the client was prioritized to understand his needs
- Project steps were enumerated and tasks were dispatched
- Time available was managed well

### Repository structure

- folder app containing two .py files : app.py and summary.py and also templates folder that contains index.html file
- Full book summarization.ipynb
- 203.txt file and 203-0-chapters folder.

### How to use the different files

- Run app.py this will open a locally deployed Flask interface where you are asked to input a book name for which you want a summary
when pressing submit the machine learning model Bart will run and output a summary of the book. This makes use of summary.py and index.html.
- When the book 'Uncle Tom’s Cabin' is inputed you will get a summary and also the creation of 203-0.txt which is the .txt file 
of this particular book and also a folder 203-0-chapters which contains the .txt file of each chapter
- The jupyter notebook Full book summarization.ipynb is included for those who want to play around with the summarization and make some changes
this is not used for the app.py file and is solely for trying out some possibilities.





