import dentalapp.dao.users
import dentalapp.utils
from dentalapp import admin, db
from dentalapp.models import Medicine, Service, UserRole, User
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user
from dentalapp.utils import hash_password
from wtforms import PasswordField, FileField
import cloudinary.uploader
from dentalapp.dao import stats
from wtforms.validators import ValidationError
from dentalapp.utils import is_image
from flask import request


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class BaseModelAdminView(ModelView):
    column_display_pk = True
    edit_modal = True

class MedicineView(BaseModelAdminView, AuthenticatedAdmin):
    column_filters = ['id', 'name', 'price', 'production_date', 'expiration_date', 'active']
    column_searchable_list = ['name', 'id']
    column_labels = {
        "id": "Mã thuốc",
        "name": "Tên thuốc",
        "price": "Giá",
        "active": "Hoạt động",
        "production_date": "Ngày sản xuất",
        "expiration_date": "Hạn sử dụng"
    }
    form_excluded_columns = ["appointment_schedule_medicines"]
    column_formatters = {
        "price": lambda v, c, m, p: f"{m.price:,.0f} ₫"
    }

class ServiceView(BaseModelAdminView, AuthenticatedAdmin):
    column_filters = ['id', 'name', 'price', 'active']
    column_exclude_list = ['image']
    column_searchable_list = ['name', 'id']
    column_labels = {
        "id": "Mã Dịch vụ",
        "name": "Tên dịch vụ",
        "price": "Giá",
        "active": "Hoạt động",
    }
    form_extra_fields = {
        'image_file': FileField("Ảnh dịch vụ")
    }
    form_excluded_columns = ["appointment_schedule_services", "image"]
    column_formatters = {
        "price": lambda v, c, m, p: f"{m.price:,.0f} ₫"
    }

    def on_model_change(self, form, model, is_created):
        if form.image_file.data:
            if not is_image(form.image_file.data.filename):
                raise ValidationError("File không hợp lệ!")
            model.image = cloudinary.uploader.upload(form.image_file.data).get("secure_url")

class UserView(AuthenticatedAdmin):
    edit_modal = True
    column_searchable_list = ['name', 'id']
    column_filters = ['id', 'name', 'phone', 'user_role', 'active']
    column_list = ['id', 'name', 'phone', 'user_role', 'active']
    column_labels = {
        "id": "Mã người dùng",
        "name": "Họ tên",
        "phone": "Số điện thoại",
        "active": "Hoạt động",
        "avatar": "Ảnh đại diện"
    }
    form_extra_fields = {
        'pwd': PasswordField('Mật khẩu'),
        'confirm': PasswordField('Xác nhận mật khẩu'),
        'avatar_file': FileField("Ảnh đại diện")
    }
    form_edit_rules = ['name', 'phone', 'user_role', 'active']
    form_create_rules = ['name', 'username', 'phone', 'pwd', 'confirm', 'user_role', 'active', 'avatar_file']
    column_details_exclude_list = ['password', 'avatar', 'username']

    def on_model_change(self, form, model, is_created):
        if not is_created:
            return

        if not dentalapp.dao.users.validate_password(form.pwd.data, form.confirm.data):
            raise ValidationError("Mật khẩu không khớp!")

        if not dentalapp.dao.users.validate_phone(form.phone.data):
            raise ValidationError("Số điện thoại không hợp lệ!")

        if form.avatar_file.data:
            if not is_image(form.avatar_file.data.filename):
                raise ValidationError("File không hợp lệ!")
            model.avatar = cloudinary.uploader.upload(form.avatar_file.data).get("secure_url")
        model.username = form.username.data
        model.password = hash_password(form.pwd.data)
        model.phone = form.phone.data

class Stats_view(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html'
                           , revenue_day=stats.revenue_by_doctor_day()
                           , revenue_month=stats.revenue_by_doctor_month()
                           , revenue_doctor=stats.revenue_by_doctor())



admin.add_view(MedicineView(Medicine, db.session, name="Thuốc"))
admin.add_view(ServiceView(Service, db.session, name="Dịch vụ"))
admin.add_view(UserView(User, db.session, name="Người dùng"))
admin.add_view(Stats_view(name="Thống kê"))