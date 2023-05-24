import urllib.request
import urllib.parse

def search_naver_news(keyword):
    client_id = "jn1lIFp4CBHFiQdNmMqQ"
    client_secret = "hsp9pIh3do"
    encText = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/news?query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        return response_body.decode('utf-8')
    else:
        return "Error Code:" + rescode
