from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Transaction

class TransactionTests(TestCase):
    def test_transaction_creation(self):
        txn = Transaction.objects.create(
            date='2025-08-11',
            description='Test Income',
            category='Food',
            amount=2415.0
        )
        self.assertEqual(txn.amount, 1000.0)
        self.assertEqual(txn.category, 'Food')
