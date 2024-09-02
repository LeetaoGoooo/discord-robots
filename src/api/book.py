import requests


def get_image_from_douban(book_name: str) -> str:
    resp = requests.get(
        f'https://book.douban.com/j/subject_suggest?q={book_name}', headers={"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"})
    if resp.status_code != 200 or not resp.json():
        return
    resp_json = resp.json()
    return resp_json[0]["pic"]