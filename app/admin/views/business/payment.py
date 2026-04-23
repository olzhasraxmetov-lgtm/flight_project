from app.models.payments import PaymentsORM
from sqladmin import ModelView

class PaymentAdmin(ModelView, model=PaymentsORM):
    column_list = [PaymentsORM.id, PaymentsORM.transaction_id, PaymentsORM.status, PaymentsORM.amount]
    column_details_exclude_list = [PaymentsORM.updated_at]
    name = "Платеж"
    name_plural = "Платежи"
    icon = "fa-solid fa-credit-card"
    can_create = False
    can_edit = False
    can_delete = False