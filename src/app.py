import cv2

from flask import Flask, render_template, request, redirect, url_for, session
''' import matplotlib.pyplot as plt '''
import os, smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
os.getcwd()
# os.chdir('./src/')
app = Flask(__name__)


app.secret_key = 'your secret key'

def SendMail(ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'someone tring to login'
    msg['From'] = "johnp@gmail.com"
    msg['To'] = "udaygupta1711@gmail.com"

    text = MIMEText("this is the photo of person")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("email", "password")
    s.sendmail("joh@mail.com", "udaygupta1711@gmail.com", msg.as_string())
    s.quit()



def take_picture():
    ImgFileName = '../res/photo/savedImage.jpg'
    try:
        os.remove(ImgFileName)
    except:
        pass
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # plt.imshow(img1)
    # plt.title('Color Image RGB')
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()
    cv2.imwrite(ImgFileName, img)
    # cap.release()
    print('sending mail')
    # SendMail(ImgFileName)

def read_file(mode,flag = 0):
    if mode=="r":
        filename = '../res/count.txt'
        file1 = open(filename,'r')
        flag = file1.read()
        file1.close()
    else:
        flag = flag + 1
        print(flag)
        filename = '../res/count.txt'
        file1 = open(filename,'w+')
        file1.write(str(flag))
        file1.close()
    return flag


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    flag = read_file('r')
    flag = int(flag.replace('\n',''))
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if username =='1234567890' and password == '1234567890':
            session['loggedin'] = True
            session['id'] = username
            session['username'] = password
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
            if flag >= 3:
                try:
                    print('taking picture')
                    take_picture()
                    flag = read_file('w',0)
                except:
                    print('error while taking picture')
                    flag = read_file('w',0)
            else:
                flag = read_file('w',flag)

    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
