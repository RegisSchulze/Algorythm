from flask import Flask, render_template, request
from summary import summarization

app=Flask(__name__)
@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    if request.method == 'POST':
        book_name=request.form.get('book')

        # run get_book method from class summarization which returns chapter folder
        # and will create a folder with the divided book chapters (.txt files)
        chapter_folder=summarization.get_book(book_name)
        
        # run create_summary method from class summarization which returns
        # a list containing the summary of each chapter, which results in the full book summary
        full_summary=summarization.create_summary(chapter_folder)
        return render_template('index.html',full_summary=full_summary)
if __name__ == '__main__':
    app.run()



