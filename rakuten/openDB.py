import requests
import json

endpoint = "https://api.openbd.jp/v1/get"

headers= {
    
}
params={
    "isbn":"9784492315040"
}

result = requests.get(endpoint, headers=headers, params=params)

res = result.json()

# print(res["onix"]["RecordReference"])
print(res[0]["onix"]["RecordReference"])
print(res[0]["onix"]["DescriptiveDetail"]["Contributor"]["TitleDetail"]["TitleElement"][0]["TitleText"]["content"])
print(res[0]["onix"]["DescriptiveDetail"]["TitleDetail"]["TitleElement"]["TitleText"]["content"])
for author in res[0]["onix"]["DescriptiveDetail"]["Contributor"]: #著者が複数人の場合
    print(author["PersonName"]["content"])
print(res[0]["onix"]["DescriptiveDetail"]["reviews"]["SubjectHeadingText"])
print(res[0]["onix"]["DescriptiveDetail"]["TitleDetail"]["TitleElement"]["TitleText"]["content"])
for text in res[0]["onix"]["CollateralDetail"]["TextContent"]:
    print(text["Text"])