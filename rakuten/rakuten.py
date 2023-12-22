import requests
import numpy as np
import pandas as pd
REQUEST_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
APP_ID="1001907355700833338"

serch_keyword = 'マクロ経済学'

serch_params = {
    "format" : "json",
    "keyword" : serch_keyword,
    "applicationId" : [APP_ID],
    "availability" : 0,
    "hits" : 30,
    "page" : 1,
    "sort" : "-updateTimestamp"
}

response = requests.get(REQUEST_URL, serch_params)
result = response.json()
print(result)

#for文を回してdictを作る
item_key = ['itemName', 'itemPrice', 'itemCaption', 'shopName', 'shopUrl', 'itemUrl']
item_list = []
for i in range(0, len(result['Items'])):
    tmp_item = {}
    item = result['Items'][i]['Item']
    for key, value in item.items():
        if key in item_key:
            tmp_item[key] = value
    item_list.append(tmp_item.copy())

# データフレームを作成
items_df = pd.DataFrame(item_list)

# 列の順番を入れ替える
items_df = items_df.reindex(columns=['itemName', 'itemPrice', 'itemCaption', 'itemUrl', 'shopName', 'shopUrl'])

# 列名と行番号を変更する:列名は日本語に、行番号は1からの連番にする
items_df.columns = ['商品名', '商品価格', '商品説明文', '商品URL', '店舗名', '店舗URL']
items_df.index = np.arange(1, 31)
items_df.to_csv('./rakuten_mayqueen.csv')
