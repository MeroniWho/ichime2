import os
from flask import (
     Flask, 
     request, 
     render_template)
from extract_text import extract_text_from_image
from books_googleapi import search_books
import pandas as pd
#画像のアップロード先のディレクトリ
UPLOAD_FOLDER='./static/book_image'

#FlaskでAPIを書くときのおまじない
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload_user_files():
    if request.method == 'POST':
        upload_file = request.files['upload_file']
        print(upload_file)
        img_path = os.path.join(UPLOAD_FOLDER,upload_file.filename)
        upload_file.save(img_path)
        search_text = extract_text_from_image(img_path)     
        #print(search_text)
        df=search_books(search_text)
        rating=df['rating'].iat[0]
        title=df['title'].iat[0]
        ratingcount=df['ratingcount'].iat[0]
        #print(df)
        #df.to_csv("df_1.csv",index=False)
        return render_template('result.html', title=title, rating=rating , ratingcount=ratingcount , img_path=img_path)
if __name__ == "__main__":
    app.run(debug=True)

