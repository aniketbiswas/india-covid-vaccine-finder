# state_ids can be found using curl -X GET "https://cdn-api.co-vin.in/api/v2/admin/location/states" -H  "accept: application/json" -H  "Accept-Language: hi_IN"
# Or open https://cdn-api.co-vin.in/api/v2/admin/location/states in browser
# district_ids can be found using curl -X GET "https://cdn-api.co-vin.in/api/v2/admin/location/districts/12" -H  "accept: application/json" -H  "Accept-Language: hi_IN"
# or open https://cdn-api.co-vin.in/api/v2/admin/location/districts/12 in browser, replace 12 with your state_id.

# Online Python3 Compiler : https://www.programiz.com/python-programming/online-compiler/  

import requests
# Edit below details
pin_code = "140603"
date = "03-05-2021"
district_ids = ['108', '187', '496']

## No more edits

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
url1 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

my_params = {'pincode' : pin_code, 'date': date}

response = requests.get(
    url,
    params = my_params,
)
centers = {}

result = response.json()
for i in result["centers"]:
    centers[i["center_id"]] = i

for id in district_ids:
    my_params1 = {'district_id': id, 'date': date}
    response = requests.get(
        url1,
        params = my_params1,
    )
    for i in response.json()["centers"]:
        if i["center_id"] not in centers:
            centers[i["center_id"]] = i
 
flag = False
for id, center in centers.items():
    flag1 = False
    sessions = center["sessions"]
    for session in sessions:
        if session['min_age_limit'] < 45:
            if flag1 == False:
                print(f"{center['state_name']}, {center['district_name']}, {center['name']}, from: {center['from']}, to: {center['to']}, fee_type: {center['fee_type']}")
                flag1 = True
            flag = True
            print(f"{session['date']}, capacity: {session['available_capacity']}, age limit: {session['min_age_limit']}, vaccine: {session['vaccine']}, slots: {session['slots']}")
if flag == False:
    print("No vaccines available!")

