from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Product, Sale, Task

class Command(BaseCommand):
    help = 'Set up roles and permissions'

    def handle(self, *args, **kwargs):
        # Create groups
        salesperson_group, _ = Group.objects.get_or_create(name='Salesperson')
        productmanager_group, _ = Group.objects.get_or_create(name='ProductManager')
        marketing_group, _ = Group.objects.get_or_create(name='Marketing')  # New group

        # Assign full permissions to Salesperson (for Sale model)
        sale_ct = ContentType.objects.get_for_model(Sale)
        sale_perms = Permission.objects.filter(content_type=sale_ct)
        salesperson_group.permissions.set(sale_perms)

        # Assign full permissions to ProductManager (for Product model)
        product_ct = ContentType.objects.get_for_model(Product)
        product_perms = Permission.objects.filter(content_type=product_ct)
        productmanager_group.permissions.set(product_perms)

        # Assign ONLY view permissions to Marketing (for both models)
        marketing_perms = Permission.objects.filter(
            content_type__in=[sale_ct, product_ct],
            codename__startswith='view_'
        )
        marketing_group.permissions.set(marketing_perms)

        # Assign view permissions to Salesperson and ProductManager (for Task model)
        task_view_perms = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Task),
            codename='view_task'
        )
        salesperson_group.permissions.set(task_view_perms)
        productmanager_group.permissions.set(task_view_perms)
        marketing_group.permissions.set(task_view_perms)

        # Assign full permissions to TaskManager (for Task model)

        self.stdout.write(self.style.SUCCESS('Roles and permissions set up successfully.'))
