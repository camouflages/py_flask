from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User
from exts import db



app=Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        telephone=request.form.get('telephone')
        password=request.form.get('password')
        user=User.query.filter(telephone==telephone,password==password).first()
        if user:
            session['user_id']=user.id
            session.permanent=True
            return redirect(url_for('index'))
        else:
            return u'手机号或者密码错误'
@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method=='GET':
        return render_template('regist.html')
    else:
        telephone=request.form.get("telephone")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user=User.query.filter(User.telephone==telephone).first()
        if user:
            return u'该手机号码已经被注册'
        else:
            if password1 != password2:
                return u'两次密码不一致请重新输入'
            else:
                user=User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('login'))


if __name__=='__main__':
    app.run()