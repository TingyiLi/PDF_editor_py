import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "CnbXvN0Q0gCHVkGFavV0g", "isbns": "9781632168146"})
#print(res.json())
R = res.json()
print(R['books'][0]['id'])
