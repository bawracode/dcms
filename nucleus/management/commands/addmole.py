from django.core.management.base import BaseCommand
from django.core.management.commands.startapp import Command as StartAppCommand

class Command(StartAppCommand):
    help = 'Creates a new app with extended functionality.'

    def handle(self, *args, **options):
        # Custom logic to extend the startapp command (addmole)
        # ...
        print(*args)
        print('-----')
        #print(**options)
        print('#######')
        #super().handle(*args, **options)  # Call the parent's handle() method
