from dentalapp import admin, db
from dentalapp.models import Medicine, Service, UserRole, User
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class BaseModelAdminView(ModelView):
    column_display_pk = True
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True

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
    column_searchable_list = ['name', 'id']
    column_labels = {
        "id": "Mã Dịch vụ",
        "name": "Tên dịch vụ",
        "price": "Giá",
        "active": "Hoạt động",
    }
    form_excluded_columns = ["appointment_schedule_services"]
    column_formatters = {
        "price": lambda v, c, m, p: f"{m.price:,.0f} ₫"
    }

class UserView(AuthenticatedAdmin):
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_searchable_list = ['name', 'id']
    column_filters = ['id', 'name', 'phone', 'user_role', 'active']
    column_list = ['id', 'name', 'phone', 'user_role', 'active']
    column_labels = {
        "id": "Mã người dùng",
        "name": "Họ tên",
        "phone": "Số điện thoại",
        "active": "Hoạt động",
    }
    form_edit_rules = ['name', 'phone', 'user_role', 'active']
    column_details_exclude_list = ['password', 'avatar', 'username']


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin.add_view(MedicineView(Medicine, db.session, name="Thuốc"))
admin.add_view(ServiceView(Service, db.session, name="Dịch vụ"))
admin.add_view(UserView(User, db.session, name="Người dùng"))
# admin.add_view(LogoutView(name="Đăng xuất"))