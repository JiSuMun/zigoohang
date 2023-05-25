import requests
import os

def get_latlng_from_address(address):
    url = f'https://dapi.kakao.com/v2/local/search/address.json?query={address}'
    headers = {'Authorization': f'KakaoAK {os.getenv("kakao_key")}'}
    response = requests.get(url, headers=headers)
    response_json = response.json()
    lat = response_json['documents'][0]['y']
    lng = response_json['documents'][0]['x']

    return (lat, lng)