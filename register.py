#!/usr/bin/python3.6
import mysql.connector
# import sshtunnel
from datetime import datetime,timedelta
import hashlib
import os
from flask import flash

salt =b'Hw\x1aPz\xf7\x1d\xd1\x15\xea\xd8&\xcc\x11\x1du\xca990=\x85\xc1T\xee\x831>\x15@\xfad'
USER_HOME = '/home/selvaprakash/BillD/static/users/'
#USER_HOME = '/mnt/c/d/BILLD/static/users/'

def create_user(username,pwd):
        cnx = mysql.connector.connect(user='selvaprakash', password='selvamysqladmin1',
                                  host='selvaprakash.mysql.pythonanywhere-services.com', database='selvaprakash$BILLD')
        #cnx = mysql.connector.connect(user='root',password='selvamys1', host='localhost', database='BILLD')
        print('connected')
        cursor = cnx.cursor()

        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            pwd.encode('utf-8'), # Convert the password to bytes
            salt, # Provide the salt
            100000, # It is recommended to use at least 100,000 iterations of SHA-256
            dklen=128 # Get a 128 byte key
        )

        key = key.hex()

        check_query = ("SELECT username from USERS WHERE lower(username)=lower(%s)")

        cursor.execute(check_query,(username,))

        for cont in cursor:
            if len(cont)>0:
                print("Email already Registered")
                flash("Email already Registered")
                return ('unc')
                break
        sel_query = ("SELECT MAX(id) from USERS")
        cursor.execute(sel_query)
        # new_id=0
        for cont in cursor:
            new_id = cont[0]+1

        validity_date = datetime.today() + timedelta(days=30)
        print (validity_date)

        ins_query = ("INSERT INTO USERS (id,username,password,created_dt,updated_dt,valid_till_date) VALUES (%s,%s, %s, %s, %s,%s)")

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        str_id=str(new_id)

        str_validity_dt =str(validity_date)
        cursor.execute(ins_query, (str_id,username,key,now,now,str_validity_dt,))
        print ('inserted')
        cnx.commit()
        os.mkdir(USER_HOME+username)
        os.mkdir(USER_HOME+username+'/CSV')
        os.mkdir(USER_HOME + username + '/CSV/templates')
        os.mkdir(USER_HOME + username + '/CSV/results')
        os.mkdir(USER_HOME+username+'/images')
        os.mkdir(USER_HOME + username + '/images/processed')
        os.mkdir(USER_HOME+username+'/html')
        os.mkdir(USER_HOME+username+'/pdf')


        return ('uc')


if __name__== '__main__':
    create_user('admin1','ddd')