from    flask          import Flask, render_template, redirect, url_for, request, flash, jsonify
from    flask_login    import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from    distutils.log  import debug 
from    fileinput      import filename
import  os
import  PyPDF2
from    model import *
from    connection import *
import  json

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['LOGIN_MESSAGE'] = 'Bu sayfayı görüntülemek için giriş yapmalısınız.'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if  current_user.is_authenticated and get_username_by_userID(current_user.id) == 'admin':
        return redirect(url_for('dosyayukle'))
    if current_user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        result = get_password_id_by_username(username)
        if result and password == result:
            user_id = get_user_id_by_name(username)
            user = User(user_id)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Geçersiz Kullanıcı Adı veya Şifre')

    return render_template('signin.html')

@app.context_processor
def inject_username():
    # In a real application, you would fetch the username dynamically
    # For this example, we'll hardcode a username.
    username = None  # Default to None if the user is not authenticated
    if current_user.is_authenticated:
        username = get_username_by_userID(current_user.id)
    return dict(username=username)

@app.route('/ogretmen')
@login_required
def ogretmen():
    if  current_user.is_authenticated and get_username_by_userID(current_user.id) == 'admin':
        return redirect(url_for('dosyayukle'))
    if not get_isTeacher_by_user_id(current_user.id):
        return redirect(url_for('dashboard'))
    
    exam_results = [res.as_dict() for res in get_all_exam_results()]
    for entry in exam_results:
        current_user_id = entry['user_ID']
        username = get_username_by_userID(current_user_id)
        classname = get_class_name_by_user_id(current_user_id)
        examname = get_exam_name_by_id(entry['exam_ID'])
        examtype = get_exam_type_by_exam_id(entry['exam_ID'])
        entry['username'] = username
        entry['classname'] = classname
        entry['examname'] = examname
        entry['examtype'] = examtype
    return render_template(
        'ogretmen.html',
        exam_results= (exam_results),
        classnames= get_all_class_names(),
        examnames= get_all_exam_names(),
        examtypes = get_all_exam_types()
        )

@app.route('/dashboard')
@login_required
def dashboard():
    if get_isTeacher_by_user_id(current_user.id):
        return redirect(url_for('ogretmen'))
    exam_result = get_exam_result_by_user_id(current_user.id)
    exam_ID = [result.exam_ID for result in exam_result]
    scores  = [result.qabs for result in exam_result]
    qtrues = [result.qtrue for result in exam_result]
    qfalses = [result.qfalse for result in exam_result]
    examname = [get_exam_name_by_id(x) for x in exam_ID]

    return render_template(
        'dashboard.html',
        exam_result=exam_result,
        exam_ID=exam_ID,
        scores=scores,
        qtrues=qtrues,
        qfalses=qfalses,
        examname=examname  )

@app.route('/dosyayukle', methods=['GET', 'POST'])
@login_required
def dosyayukle():
    if get_username_by_userID(current_user.id) != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':   
        upload_date = request.form.get('date')
        exam_type = request.form.get('examtype')
        f = request.files['file']

        # Do something with upload_date and exam_type if needed
        # For example, you can modify the filename to include the date and exam type

        # Specify the parent folder path (in this case, 'uploads')
        folder_path = os.path.join(os.getcwd(), 'Karne')

        # Check if folder exists, if not create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save the file to the specified folder using the new filename
        f.save(os.path.join(folder_path, f.filename))
        add_new_data(filename= f'{folder_path}/{f.filename}',date= upload_date, exam_type= exam_type)
        return render_template("dosyayukle.html",filename=f.filename)
    # For GET requests
    return render_template("dosyayukle.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def hello_world():
    return redirect(url_for('login'))

def add_new_data(filename:str,date:str,exam_type:str): 
# creating a pdf file object
    pdfFileObj = open(filename, 'rb')
    filename = filename.split('/')[-1].split('.pdf')[0]
    
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # printing number of pages in pdf file

    examtypeID = 1 if exam_type == 'TYT' else 2
    date = date

    add_exam(exam_name= filename,exam_type_ID= examtypeID, date= date)

    for npage in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[npage]
        lineSplitted = pageObj.extract_text().splitlines()

        userinfo_inx = lineSplitted.index('Öğrenci Numara Sınıf') + 1
        userinfo = lineSplitted[userinfo_inx]
        for line in lineSplitted:
            if line.startswith('Toplam'):
                userexamresult = line

        #getting datas
        name  = []
        school_no = 0
        userclass = 'Yok'
        for x in userinfo.split(' '):
            x.replace(' ','')
            if x in ['9A','9B','9C','9D','10B','10C','10D','10A','11A','11B','11C','11D','11E','12A','12B','12C','12D','12E']:
                userclass = x
            elif x.isalpha():
                name.append(x)
            elif x.isnumeric():
                school_no = x
        username = f'{convert_to_username(name)}{school_no}'
        password = caesar_hashing(username[:4])
        qtrue, qfalse, qabs, score = userexamresult.replace(',','.').split(' ')[2:6]
        #processing datas

        if not class_exists(userclass):
            add_class(userclass)
        userClassID = get_class_id_by_name(userclass)

        if not user_exists(username=username):
            add_user(
                username= username,
                password=password,
                school_no= school_no,
                class_ID= userClassID,
                isTeacher = 0
            )
        userID = get_user_id_by_name(username=username)

        add_exam_result(
            user_ID= userID,
            exam_ID= get_exam_id_by_name(exam_name= filename),
            qtrue=qtrue,
            qfalse=qfalse,
            qabs=qabs,
            score=score
        )
        print(f'user successfully added{username}')

    # closing the pdf file object
    pdfFileObj.close()

app.run(debug= False, host='0.0.0.0', port=5000)