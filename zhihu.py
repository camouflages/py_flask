from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User,Question,Answer
from exts import db
from functools import wraps


app=Flask(__name__)
app.config.from_object(config)
db.init_app(app)



#登录限制
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
         if session.get('user_id'):
             return func(*args,**kwargs)
         else:
            return redirect(url_for('login'))
    return  wrapper
@app.route('/')
def index():
    context={
        "questions":Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)

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
@app.route('/logout/')
def logout():
    session.clear()
    return  redirect(url_for('login'))


@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method=='GET':
        return render_template('question.html')
    else:
        title=request.form.get('title')
        content = request.form.get('content')
        question=Question(title=title,content=content)
        user_id=session.get('use_id')
        user=User.query.filter(User.id==user_id).first()
        question.author=user
        db.session.add(question)
        db.session.commit()

@app.route('/detail/<question_id>')
def detail(question_id):
    question_model=Question.query.filter(Question.id==question_id).first()
    return render_template('detail.html',question=question_model)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content=request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer=Answer(content=content)
    user_id=session['user_id']
    answer.author=User.query.filter(User.id==user_id).first()
    answer.question=Question.query.filter(Question.id == question_id).first()
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))


if __name__=='__main__':
    app.run()