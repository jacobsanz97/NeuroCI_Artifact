import requests
import json
import sys

import os

def cbrain_login(username, password):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }
    data = {
      'login': username,
      'password': password
    }
    response = requests.post('https://portal.cbrain.mcgill.ca/session', headers=headers, data=data)
    if response.status_code == 200:
        print("Login success")
        print(response.content)
        jsonResponse = response.json()
        return jsonResponse["cbrain_api_token"]
    else:
        print("Login failure")
        return 1
    
def cbrain_FSLStats(token, fileID):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    params = (
        ('cbrain_api_token', token),
    )
    data = {
      "cbrain_task": {
        "type": "CbrainTask::Fslstats",
        "user_id": 1887,
        "bourreau_id": 39,
        "tool_config_id": 1698,
        "params": {
          "interface_userfile_ids": [
            fileID
          ],
          "input_file": fileID,
          "t": False,
          "l": 16.5,
          "u": 17.5,
          "a": False,
          "n": False,
          "r": False,
          "R": False,
          "e": False,
          "E": False,
          "v": False,
          "V": True,
          "m": False,
          "M": False,
          "s": False,
          "S": False,
          "w": False,
          "x": False,
          "X": False,
          "c": False,
          "C": False,
          "output": "output.txt",
          "_cbrain_output_output": [
            2731401
          ]},
          "status": "Completed",
          "created_at": "2020-06-05T06:57:39.000-07:00",
          "updated_at": "2020-06-05T06:58:46.000-07:00",
          "run_number": None,
          "results_data_provider_id": 27,
          "cluster_workdir_size": 40960,
          "workdir_archived": False,
         "workdir_archive_userfile_id": None,
         "description": ""
      }
    }
    # convert into JSON:
    y = json.dumps(data)
    response = requests.post('https://portal.cbrain.mcgill.ca/tasks', headers=headers, params=params, data=y)
    if response.status_code == 200:
        print(response.text)
        jsonResponse = response.json()
        return jsonResponse[0]["id"]
    else:
        print("Task posting failed.")
        return 1

def cbrain_getTaskOutputFile(token, taskID):
    headers = {
        'Accept': 'application/json',
    }
    params = (
        ('id', taskID),
        ('cbrain_api_token', token)
    )
    url = 'https://portal.cbrain.mcgill.ca/tasks/' + taskID
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        jsonResponse = response.json()
        if jsonResponse["status"] == "Completed":
            return jsonResponse["params"]["_cbrain_output_output"][0] #gets the first if there are many outputs.
        else:
            print("Task not completed yet")
            return 1
    else:
        print("Failed to get task info")
        return 1

def cbrain_download_text(fileID, token):
    headers = {
        'Accept': 'text',
    }
    params = (
        ('cbrain_api_token', token),
    )
    url = 'https://portal.cbrain.mcgill.ca/userfiles/' + fileID + '/content'
    response = requests.get(url, headers=headers, params=params, allow_redirects=True)
    if response.status_code == 200:
        return response.text
    else:
        print('Download failure')
        return 1

def cbrain_logout(token):
    headers = {
        'Accept': 'application/json',
    }
    params = (
        ('cbrain_api_token', token),
    )
    response = requests.delete('https://portal.cbrain.mcgill.ca/session', headers=headers, params=params)
    if response.status_code == 200:
        print("Logout success")
    else:
        print("Logout failure")
        return 1

login = sys.argv[1]
password = sys.argv[2]

token = cbrain_login(login, password)

#taskID = cbrain_FSLStats(token, "2731398")
print(os.getcwd())


outputFileID = cbrain_getTaskOutputFile(token, "1135602")

txtt = cbrain_download_text(str(outputFileID), token)
file = open("results.txt", "w")
file.write(txtt)
file.close()

cbrain_logout(token) 
