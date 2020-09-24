#!/usr/bin/python3.6
import mysql.connector
# import sshtunnel
import hashlib
from datetime import date


def check_pwd(username,pwd):

        cnx = mysql.connector.connect(user='selvaprakash',password='selvamysqladmin1', host='selvaprakash.mysql.pythonanywhere-services.com', database='selvaprakash$BILLD')
        # cnx = mysql.connector.connect(
        #     user='selvaprakash', password='selvamysqladmin1',
        #     host='127.0.0.1', port=tunnel.local_bind_port,
        #     database='selvaprakash$BILLD',
        # )
        print('connected')
        cursor = cnx.cursor()

        query = ("SELECT password,valid_till_date from USERS WHERE username = %s")

        salt =b'Hw\x1aPz\xf7\x1d\xd1\x15\xea\xd8&\xcc\x11\x1du\xca990=\x85\xc1T\xee\x831>\x15@\xfad'

        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            pwd.encode('utf-8'), # Convert the password to bytes
            salt, # Provide the salt
            100000, # It is recommended to use at least 100,000 iterations of SHA-256
            dklen=128 # Get a 128 byte key
        )

        key = key.hex()

        cursor.execute(query, (username,))

        for (fields) in cursor:
            print (fields[0])
            print (key)
            if (fields[0] == key):
                print ('pwd match')
                if (fields[1] >= date.today()):
                    return 'good1'
                else:
                    return 'notgood'

            else:
                print ('notgood')
                return 'notgood'


if __name__== '__main__':
    check_pwd('admin1','ddd')
