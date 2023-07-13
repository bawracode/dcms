# add_translation.py
from django.core.management.base import BaseCommand
import polib

class Command(BaseCommand):
    help = 'Add translation entry to a specific language PO file'

    def handle(self, *args, **options):
        po_file_path = options['po_file_path']
        msgid = options['msgid']
        msgstr = options['msgstr']
        language_code = options['language_code']

        po = polib.pofile(po_file_path)

        # Check if the translation entry already exists
        for entry in po:
            if entry.msgid == msgid and entry.msgstr == msgstr:
                self.stdout.write(self.style.WARNING('Translation entry already exists!'))
                return

        # Create a new entry and add it to the PO file
        entry = polib.POEntry()
        entry.msgid = msgid
        entry.msgstr = msgstr
        po.append(entry)

        # Save the updated PO file
        po.save()

        self.stdout.write(self.style.SUCCESS('Translation entry added successfully!'))
