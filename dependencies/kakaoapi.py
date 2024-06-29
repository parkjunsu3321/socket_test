import requests

api_key = 'KakaoAK eb5944d1d43c5a796a5eb08fdf185761'

def get_region_from_coords(x, y):
    api_url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json'
    headers = {
        'Authorization': api_key
    }
    params = {
        'x': x,   # 경도(Longitude)
        'y': y    # 위도(Latitude)
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            # 여기서 원하는 정보를 추출합니다.
            region = data['documents'][0]['region_2depth_name']  # 예시: '서울 송파구'
            return region
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def search_places_nearby(x, y, distance,query):
    api_url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    headers = {
        'Authorization': api_key
    }
    params = {
        'x': x,         # 경도(Longitude)
        'y': y,         # 위도(Latitude)
        'query': query, # 검색할 키워드 (예: 관광지, 맛집 등)
        'radius': distance, # 검색 반경 (미터 단위)
        'page': 1       # 페이지 번호 (기본값 1)
    }
    my_dict = {}
    my_dict['place_name'] = []
    my_dict['category_name']  = []
    address_name = []
    my_dict['x'] = []
    my_dict['y'] = []
    try:
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            places = data['documents']
            for place in places:
                my_dict['place_name'].append(place['place_name'])
                my_dict['category_name'].append(place['category_name'])
                address_name.append(place['address_name'])    
            return my_dict, address_name
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def get_coords_from_address(address):
    api_url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {
        'Authorization': api_key
    }
    params = {
        'query': address
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['meta']['total_count'] > 0:
                x = data['documents'][0]['x']  # 경도(Longitude)
                y = data['documents'][0]['y']  # 위도(Latitude)
                xy_list = []
                xy_list.append(x)
                xy_list.append(y)
                print(xy_list)
                return xy_list
            else:
                print(f"'{address}'에 대한 검색 결과가 없습니다.")
                return None
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def get_nearby_bus_stops(x, y, radius=1000):
    api_url = 'https://dapi.kakao.com/v2/local/search/category.json'
    headers = {
        'Authorization': api_key
    }
    params = {
        'category_group_code': 'PO3',  # 대중교통 - 버스정류장 카테고리 코드
        'x': x,                        # 경도(Longitude)
        'y': y,                        # 위도(Latitude)
        'radius': radius               # 검색 반경 (미터 단위, 기본값 1000m)
    }
    try:
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['meta']['total_count'] > 0:
                bus_stops = data['documents']
                for stop in bus_stops:
                    place_name = stop['place_name']    # 정류장명
                    category_name = stop['category_name']  # 카테고리명
                    address_name = stop['address_name']   # 주소
                    x = stop['x']  # 경도
                    y = stop['y']  # 위도
                    print(f"정류장명: {place_name}, 카테고리: {category_name}, 주소: {address_name}, 좌표: ({x}, {y})")
            else:
                print(f"반경 {radius}m 이내에 버스 정류장이 없습니다.")
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
