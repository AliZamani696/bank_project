



from django.db import transaction
from .models import Account, Transaction
from decimal import Decimal
from django.core.exceptions import ValidationError



def transfer_money(sender_id, receiver_id, amount):
    amount = Decimal(str(amount))
    if amount <= 0:
        raise ValidationError("amount must be big of 0")

    with transaction.atomic():
        ids = sorted([sender_id,receiver_id])
        accounts_dict = Account.objects.select_for_update().in_bulk(ids)
        sender_acc = accounts_dict.get(sender_id)
        receiver_acc = accounts_dict.get(receiver_id)

        if sender_acc.balance < amount:
            raise ValidationError("balance not enoough")

        sender_acc.balance -= amount
        receiver_acc.balance += amount
        sender_acc.save()
        receiver_acc.save()

        Transaction.objects.create(
            sender = sender_acc,
            receiver = receiver_acc,
            amount = amount,
            transaction_type = "TRANSFER"
        )
    return True
