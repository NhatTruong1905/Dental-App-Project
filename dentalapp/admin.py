from dentalapp import admin, db
from dentalapp.models import Medicine, Service, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class BaseModelAdminView(ModelView):
    column_display_pk = True
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class MedicineView(BaseModelAdminView):
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
    form_excluded_columns = ["appointment_schedule_medicines", "active"]
    column_formatters = {
        "price": lambda v, c, m, p: f"{m.price:,.0f} ₫"
    }

class ServiceView(BaseModelAdminView):
    column_filters = ['id', 'name', 'price', 'active']
    column_searchable_list = ['name', 'id']
    column_labels = {
        "id": "Mã Dịch vụ",
        "name": "Tên dịch vụ",
        "price": "Giá",
        "active": "Hoạt động",
    }
    form_excluded_columns = ["appointment_schedule_services", "active"]
    column_formatters = {
        "price": lambda v, c, m, p: f"{m.price:,.0f} ₫"
    }


admin.add_view(MedicineView(Medicine, db.session, name="Thuốc"))
admin.add_view(ServiceView(Service, db.session, name="Dịch vụ"))