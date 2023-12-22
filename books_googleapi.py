# 書籍検索関数化済
import requests
import pandas as pd

def search_books(partial_title):
    """
    検出したテキストを入力して、一致するタイトルの本の情報をデータフレームで返す
    """
    
    base_url = "https://www.googleapis.com/books/v1/volumes"
    query = f"intitle:{partial_title}"
    print(query)
    params = {"q": query} 
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200: # 200は検索が成功しましたよ、の番号
        results = response.json()
        #print(results)
        items = results.get('items', [])
        books = []
        found = False # 本が見つかったかどうかのフラグ
        for item in items:
            if found: # 本が見つかった場合、ループを抜ける
                break
            
            info = item.get('volumeInfo', {})
            sale_info = item.get('saleInfo', {})
            list_price = sale_info.get('listPrice', {})
            image_links = info.get('imageLinks', {})
            
            book = {
                'title': info.get('title', '').lower(),
                'authors': ", ".join(info.get('authors', [])).lower(),
                'price': list_price.get('amount', 'N/A'),
                'currency': list_price.get('currencyCode', 'N/A'),
                'thumbnail': image_links.get('thumbnail', 'N/A'),
                'rating': info.get('averageRating','残念ですが、評価が少ないです'),
                'ratingcount': info.get('ratingsCount','評価した人があんまりないです')
                }
        
            books.append(book)
            found = True # 本を見つけたのでフラグを更新
                
        return pd.DataFrame(books)
    else:
        return None
