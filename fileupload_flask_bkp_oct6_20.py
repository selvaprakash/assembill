#!/usr/bin/python3.6

import os
from flask import Flask, flash,request, redirect, url_for, render_template,send_from_directory,send_file, session
from werkzeug.utils import secure_filename
import Consolidated
import requests
import datetime
import pandas as pd
#import img_to_csv
import img2csv_wip
from PIL import Image
from login import check_pwd
from register import create_user


URL='https://www.pythonanywhere.com/user/selvaprakash/files'

HOME_FOLDER = '/home/selvaprakash/'
#HOME_FOLDER = '/mnt/c/d/'

UPLOAD_FOLDER = HOME_FOLDER+ 'BillD/'
SCR_UPLOAD_FOLDER = HOME_FOLDER+ 'BillD/static/backImg/'
csv_folder=HOME_FOLDER+ 'BillD/CSV'
templates_folder=HOME_FOLDER+ 'templates/'
t=datetime.datetime.now()
API_UPLOAD_FOLDER = HOME_FOLDER+ 'BillD/static/API/'
TWITS_UPLOAD_FOLDER = HOME_FOLDER+ 'BillD/static/API/copytextapp/'
#USER_FOLDER = '/home/selvaprakash/BillD/users/'
global USER_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
USER_FOLDER = HOME_FOLDER+'BillD/static/users/'
application = Flask(__name__)
application.secret_key = 'lZiqUQM5YfhjMXffaNpDWAsMKd280ZGA'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['SCR_UPLOAD_FOLDER'] = SCR_UPLOAD_FOLDER
application.config['TWITS_UPLOAD_FOLDER'] = SCR_UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print ('inside post')
        username = request.form['email']
        print (username)
        pwd = request.form ['password']
        print (pwd)
        if check_pwd(username,pwd) =='good1':
            print ('right')
            session['username'] = request.form['email']
            print (session['username'])
            return redirect(url_for('upload_scrfile',user = session['username']))

        else:
            print ('password wrong')
            return render_template('userform_login.html')
    return render_template('userform_login.html')


@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print ('inside post')
        username = request.form['email']
        print (username)
        pwd = request.form ['password']
        if create_user (username,pwd) == 'uc':
            return redirect(url_for('login'))
    return render_template('userform_register.html')


@application.route('/bills', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        emailid=request.form['emailid']
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            if emailid:
                print (emailid)
                csv_file_name=Consolidated.main(UPLOAD_FOLDER+'/'+file.filename,emailid)
            else:
                print ('email id is null')
                csv_file_name=Consolidated.main(UPLOAD_FOLDER+'/'+file.filename,'assembill.contact@gmail.com')
            excel_file_name='Converted_Bill_'+t.strftime('%Y%m%d%H%M%S')+'.xlsx'
            #print current_app.root_path
            #return redirect(url_for('uploaded_file',filename=csv_file_name))
            #file_full_path=UPLOAD_FOLDER+csv_file_name
            print (csv_file_name)
            print (file.filename)
            return send_file(csv_file_name,as_attachment=True,attachment_filename=excel_file_name)

    return render_template('upload_file.html')



@application.route('/imageup', methods=['GET', 'POST'])
def upload_scrfile():
    print(request.args['user'])
    user = request.args['user']
    if request.method == 'POST':
        # check if the post request has the file part
        if 'screen_img_file' not in request.files:
            print ('no files')
            flash('No file part')
            return redirect(request.url)
        file = request.files['screen_img_file']


        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print (filename)
            file.save(os.path.join(USER_FOLDER+user+'/images/', filename))
            #image = Image.open(os.path.join(USER_FOLDER+user+'/images/', filename))
            #aspect_ratio = image.size[1]/image.size[0]
            #filename = USER_FOLDER + user + '/images/'+ filename
            return redirect(url_for('config_screen',up_file = filename,user = user))
    #if 'username' in session:
    return render_template('scr_fileupload.html')
    #return 'You are not logged in'



@application.route('/scr_config1')
def config_screen_start():
    return render_template('screen_config.html')


@application.route('/scr_config_rect', methods=['GET', 'POST'])
def config_screen():
    print(request.args['up_file'])
    up_file = request.args['up_file']
    df_field = pd.DataFrame(columns=["Field","Position"])
    df_coord = pd.DataFrame(columns=["Start_X","Start_Y", "Position"])
    df_maxxy = pd.DataFrame(columns=["Field", "Start_X","Start_Y"])
    if request.method == 'POST':
        print ('inside post')
        #print request.form['field1']
        # item_coor = request.form['item']
        # print item_coor
        # price_coor = request.form['price']
        # qty_coor = request.form['qty']
        # amount_coor = request.form['amount']
        curr_time = t.strftime('%Y%m%d%H%M%S')
        f = request.form
        template_name = ''
        for field in request.form.items():
            print ('Splitted', field[1].split(';'))
            if field[0].startswith('field'):
                df_field = df_field.append({'Field': field[1],'Position': int(field[0][5:]) },ignore_index=True)
                #field[0][5:]) Serial Numbe Starts from Position 5 (field1, field2 etc)
            if field[0].startswith('coord'):
                print ('field[1]',field[1])
                df_coord = df_coord.append({'Start_X': int(field[1].split(';')[0]),'Start_Y': int(field[1].split(';')[1]), 'End_X': int(field[1].split(';')[2]),'End_Y': int(field[1].split(';')[3]),'Position': int(field[0][5:])}, ignore_index=True)
            if field[0].startswith('tmplName'):
                template_name = field[1]

        print ('df_field',df_field)
        print ('df_coord', df_coord)
        print ('df_maxxy',df_maxxy)
        df = pd.merge(df_field, df_coord, how='inner',  left_on = 'Position', right_on = 'Position')

        # for field in request.form.items():
        #     if field[0].startswith('maxxy'):
        #         df = df.append({'Field':'maxxy','Start_X': int(field[1].split(';')[0]),'Start_Y': int(field[1].split(';')[1]), 'End_X': int(field[1].split(';')[0]),'End_Y': int(field[1].split(';')[1])}, ignore_index=True)
        # # df["Position"] = df["Position"].astype(int)
        # df["Y"] = df["Y"].astype(int)
        print ('df',df)
        df = df.sort_values(by=['Position']).reset_index().drop(labels=['Position','index'],axis=1)
        print ('df', df)
        up_file_orig = up_file
        user = session['username']
        up_file=USER_FOLDER+user+'/images/'+up_file
        df.to_csv(pd.DataFrame.to_csv(df,USER_FOLDER+user+'/'+'CSV/templates/'+template_name+'.csv'))
        template_file = USER_FOLDER + user + '/' + 'CSV/templates/' + template_name + '.csv'
        img2csv_wip.main( df,up_file,user,template_file)
        csv_file_name = USER_FOLDER+user+'/CSV/results/'+os.path.basename(up_file)+'.csv'
        if request.form['action'] == 'csv':
            return send_file(csv_file_name,as_attachment=True)
        elif request.form['action'] == 'clip':
            df_out = pd.read_csv(csv_file_name)
            df_out.to_html(USER_FOLDER+user+'/html/'+session['username']+'_'+up_file_orig+curr_time+'.html',index=False)
            return send_file(USER_FOLDER+user+'/html/'+session['username']+'_'+up_file_orig+curr_time+'.html',as_attachment=True)
            #return render_template(USER_FOLDER+user+'/html/'+session['username']+'_'+up_file_orig+curr_time+'.html')
            os.remove(templates_folder+session['username']+up_file_orig+t.strftime('%Y%m%d%H%M%S')+'.html')
    
    return render_template('screen_config_rect.html')



@application.route('/api', methods=['GET', 'POST'])
def upload_file_api():
    if request.method == 'POST':
        # check if the post request has the file part
        print ('inside post')
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['SCR_UPLOAD_FOLDER'], filename))
            up_file=SCR_UPLOAD_FOLDER+file.filename
            csv_file_name = '/home/selvaprakash/BillD/CSV/img2csv.csv'
            df_coord = pd.DataFrame(columns=['Field','Position','Start_X','Start_Y','End_X','End_Y'])
            df_coord = df_coord.append({'Field':'','Start_X':0,'Start_Y':0,'End_X':5000,'End_Y':5000,'Position':1}, ignore_index=True)
            text_content = img2csv_wip.main_twit_api( df_coord,up_file)
            return (text_content)

#    return self


@application.route('/twitapi', methods=['GET', 'POST'])
def upload_file_twitapi():
    if request.method == 'POST':
        # check if the post request has the file part
        print ('inside twitapi post')
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['TWITS_UPLOAD_FOLDER'], filename))
            up_file=TWITS_UPLOAD_FOLDER+file.filename
            csv_file_name = '/home/selvaprakash/BillD/CSV/img2csv.csv'
            # df_coord = pd.DataFrame(columns=['Field','Position','Start_X','Start_Y','End_X','End_Y'])
            # df_coord = df_coord.append({'Field':'','Start_X':0,'Start_Y':0,'End_X':5000,'End_Y':5000,'Position':1}, ignore_index=True)
            text_content = img2csv_wip.main_twit_api( up_file)
            return (text_content)


@application.route("/twittext/<twitid>")
def profile(twitid):
    f_read = open(str(twitid)+'.txt', 'r')
    twit_text = (f_read.read())
    f_read.close()
    users = {
        "mitsuhiko": {
            "name": "Armin Ronacher",
            "bio": "Creatof of the Flask framework",
            "twitter_handle": "@mitsuhiko"
        },
        "gvanrossum": {
            "name": "Guido Van Rossum",
            "bio": "Creator of the Python programming language",
            "twitter_handle": "@gvanrossum"
        },
        "elonmusk": {
            "name": "Elon Musk",
            "bio": "technology entrepreneur, investor, and engineer",
            "twitter_handle": "@elonmusk"
        }
    }
    user = None

    if twitid in users:
        user = users[twitid]

    return render_template("profile.html", twit_text=twit_text, user=user)

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()