# core/management/commands/setup_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Product, Sale

class Command(BaseCommand):
    help = 'Set up roles and permissions'

    def handle(self, *args, **kwargs):
        # Create groups
        salesperson_group, _ = Group.objects.get_or_create(name='Salesperson')
        productmanager_group, _ = Group.objects.get_or_create(name='ProductManager')

        # Sales permissions
        sale_ct = ContentType.objects.get_for_model(Sale)
        sale_perms = Permission.objects.filter(content_type=sale_ct)
        salesperson_group.permissions.set(sale_perms)

        # Product permissions
        product_ct = ContentType.objects.get_for_model(Product)
        product_perms = Permission.objects.filter(content_type=product_ct)
        productmanager_group.permissions.set(product_perms)

        self.stdout.write(self.style.SUCCESS('Roles and permissions set up successfully.'))
