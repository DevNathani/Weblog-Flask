from flask import Flask
from flask_mail import Mail,Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kzjvksdvdvskjdvbskvdsjdvnkj'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USER'] = 'noreplyutility003@gmail.com'
app.config['MAIL_PASSWORD'] = 'ldrotveprxroqbhu'

email = Mail(app)

@app.route('/mail/<string:mail>',methods = ['GET'])
def send_mail(mail):
    sender = 'noreply@demo.com'
    reciever = mail
    msg = Message('Reset Password',sender = sender,recipients = [reciever])
    msg.body = 'Hello World'
    # try:
    email.send(msg)
    # except:
    #     return "Error"
    
@app.route('/')    
def home():
    return "INDEX"

if __name__ == '__main__':
    app.run(debug = True)
