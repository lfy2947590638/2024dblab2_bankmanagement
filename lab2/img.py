from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import DataRequired


# 允许上传的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename): # 判断文件是否允许上传
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadForm(FlaskForm):    # 上传图片表单
    # user_id = StringField('编号', validators=[DataRequired()])
    file = FileField('上传图片', validators=[DataRequired()])
    submit = SubmitField('上传')