# state_ids can be found using curl -X GET "https://cdn-api.co-vin.in/api/v2/admin/location/states" -H  "accept: application/json" -H  "Accept-Language: hi_IN"
# Or open https://cdn-api.co-vin.in/api/v2/admin/location/states in browser
# district_ids can be found using curl -X GET "https://cdn-api.co-vin.in/api/v2/admin/location/districts/12" -H  "accept: application/json" -H  "Accept-Language: hi_IN"
# or open https://cdn-api.co-vin.in/api/v2/admin/location/districts/12 in browser, replace 12 with your state_id.

# Online Python3 Compiler : https://www.programiz.com/python-programming/online-compiler/

import requests
import smtplib, ssl
import time

# Edit below details
pin_code = "201301" # Enter your pin code
date = "04-05-2021" # Enter tomorrow's date it'll find next 7 days information. Simply use a later date to find more slots.
district_ids = ['108', '187', '496', '581', '650'] # Optional use https://cdn-api.co-vin.in/api/v2/admin/location/districts/12 and https://cdn-api.co-vin.in/api/v2/admin/location/states
timedelay = 3600  # reduce it at your own risk

port = 465  # For SSL leave it as it is
smtp_server = "smtp.gmail.com"
sender_email = "your_email@gmail.com"  # Enter your gmail address
receiver_email = "any_email@any.com"  # Enter receiver address
password = input("Enter password: ")  # Enter your password

## Make sure you use your useless gmail for this and enable less secure application by visiting this link 
## https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4NxzCHX3C08uNJHsA8uPlkV4_QGJ_8fpWZYa8uFXcss_NyY9_RQb8Nlw4L4T5IZ5a8tQQQbbfdOaHXV-cTsFgfDdHcAwQ

## No more edits

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
url1 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
def fun(pincode = "201301", district_ids = [], date = "04-05-2021"):
    try:
        res = ""
        my_params = {'pincode' : pin_code, 'date': date}

        response = requests.get(
            url,
            params = my_params,
        )
        response.raise_for_status()
        centers = {}
        result = response.json()
        for i in result["centers"]:
            centers[i["center_id"]] = i
        count = 0
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
                        res += f"{center['state_name']}, {center['district_name']}, {center['name']}, from: {center['from']}, to: {center['to']}, fee_type: {center['fee_type']}\n"
                        print(f"{center['state_name']}, {center['district_name']}, {center['name']}, from: {center['from']}, to: {center['to']}, fee_type: {center['fee_type']}")
                        flag1 = True
                    flag = True
                    if session['available_capacity'] > 0:
                        count += 1
                        res += f"{session['date']}, capacity: {session['available_capacity']}, age limit: {session['min_age_limit']}, vaccine: {session['vaccine']}, slots: {session['slots']}\n"
                    print(f"{session['date']}, capacity: {session['available_capacity']}, age limit: {session['min_age_limit']}, vaccine: {session['vaccine']}, slots: {session['slots']}")
        if flag == False:
            print("No vaccines available!")
        else:
            print(f"{count} sessions available.")
        if count > 0:
            message = f"{count} sessions available.\n{res}"
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

if __name__ == '__main__':
    while(1):
        fun(pin_code, district_ids, date)
        time.sleep(timedelay)
