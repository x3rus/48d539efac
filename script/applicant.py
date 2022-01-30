#!/usr/bin/python
#
# Author: Thomas Boutry <thomas.boutry@x3rus.com>
##################################################

# Modules
# improvement : import only method we use ...

import csv
import requests
import logging
import json


class applicant():
    """application to interact with sample-app"""
    def __init__(self, baseurl, version, log_level=logging.INFO):
        """Init applicant"""
        self.baseurl = baseurl
        self.version = version
        logging.basicConfig(level=log_level)

    def getAppUrl(self):
        """Return structured url to reach app"""
        return self.baseurl + "/" + self.version

    def extractClientFromCsv(self, csv_file):
        """ extract list of client from a csv file

        return clients dictionnary
        """
        clients = []
        try:
            fd = open(csv_file)
            csv_content = csv.reader(fd)
            next(csv_content)
            for row in csv_content:
                clients.append(row)
        except Exception as e:
            print("An error occur, the script will return an empty array.")
            print('the exception occurred: {}'.format(e))
        else:
            fd.close()
        return clients

    def getClientList(self):
        """ return list of client in the app

        return http code, client list ( empty if http code is not 200)
        """
        response = requests.get(self.getAppUrl() + "/client")

        clients = []
        if response.status_code == 200:
            if len(response.content) > 0:
                http_string = response.content.decode('utf-8')
                clients = json.loads(http_string)
        else:
            logging.warning("Getting clients list return an issue http code : %d / messge %s", response.status_code,
                            response.content)

        return (response.status_code, clients)

    def getOneClient(self, c_id):
        """ retreive one client and return it in json format
        """
        response = requests.get(self.getAppUrl() + "/client/" + c_id)

        if response.status_code == 200:
            http_string = response.content.decode('utf-8')
            json_obj = json.loads(http_string)
            return response.status_code, json_obj

        if response.status_code == 404:
            return response.status_code, {}

        logging.error("Problem when contacting the app: %s", response.content)
        return response.status_code, {}

    def addClient(self, c_id, c_name, c_url):
        """ add a client to the app

        return http code, client information added OR None
        """
        # create json structure
        client_json = {
            "id": c_id,
            "name": c_name,
            "url": c_url
        }
        r = requests.post(self.getAppUrl() + "/client", json=client_json)

        if r.status_code == 200:
            return(r.status_code, client_json)
        if r.status_code == 409:
            logging.warning("client ID %s , already exist", c_id)
        else:
            logging.warning("Error adding client http code: %d / %s", r.status_code, r.content)

        return(r.status_code, None)

    def delClient(self, c_id):
        r = requests.delete(self.getAppUrl() + "/client/" + c_id)
        print(r)

    def updateClient(self, c_id, c_name="", c_url=""):
        client_json = {
            "id": c_id,
            "name": c_name,
            "url": c_url,
        }
        r = requests.put(self.getAppUrl() + "/client/", json=client_json)
        print(r)


if __name__ == "__main__":
    app = applicant("https://interview-48d539efac.interview.vme.dev/api", "v1", logging.DEBUG)
    print(app.getClientList())

    app.addClient("1234", "ze_client", "http://goototogle.com")
    app.addClient("987", "ze_client", "http://goototogle.com")
    print(app.getClientList())

    code, toto = app.getOneClient("1234")
    print(toto['url'])

    code, toto = app.getOneClient("987")
    print(toto['id'])

    app.delClient("1234")
    app.delClient("987")
    print(app.getClientList())
