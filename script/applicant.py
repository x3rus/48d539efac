#!/usr/bin/python
#
# Author: Thomas Boutry <thomas.boutry@x3rus.com>
##################################################

# Modules
# improvement : import only method we use ...

import csv
import requests
import logging


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
        response = requests.get(self.getAppUrl() + "/client")

        clients = []
        if response.status_code == 200:
            clients = response.content
        else:
            logging.warning("Getting clients list return an issue http code : %d / messge %s", response.status_code,
                            response.content)

        return (response.status_code, clients)

    def getOneClient(self, c_id):
        response = requests.get(self.getAppUrl() + "/client/" + c_id)
        return response.content

    def addClient(self, c_id, c_name, c_url):
        """ add a client to the app """
        # create json structure
        client_json = {
            "id": c_id,
            "name": c_name,
            "url": c_url
        }
        r = requests.post(self.getAppUrl() + "/client", json=client_json)
        print(r)

    def delClient(self, c_id):
        r = requests.delete(self.getAppUrl() + "/client/" + c_id)
        print(r)

    def updateClient(self, c_id, c_name=None, c_url=None, c_reachable=None, c_status=None):
        client_json = {
            "id": c_id,
            "name": c_name,
            "url": c_url,
            "reachable": "",
            "status": ""
        }
        r = requests.put(self.getAppUrl() + "/client/", json=client_json)
        print(r)


if __name__ == "__main__":
    app = applicant("https://interview-48d539efac.interview.vme.dev/api", "v1", logging.DEBUG)
    print(app.getClientList())

    app.addClient("1234", "ze_client", "http://goototogle.com")
    print(app.getClientList())

    print(app.getOneClient("1234"))

    app.addClient("9876", "ze_second_client", "http://google.com")
    print(app.getClientList())

    print(app.getOneClient("9876"))

    app.delClient("1234")
    print(app.getClientList())

    app.delClient("9876")
    print(app.getClientList())
