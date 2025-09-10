from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Ensure all users have usable Django passwords; set default where missing'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        updated = 0
        skipped = 0
        total = User.objects.count()

        for u in User.objects.all():
            if not u.has_usable_password():
                u.set_password('Fakestore123!')
                u.save(update_fields=['password'])
                updated += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'Processed {total} users: set default password for {updated}, skipped {skipped} with usable passwords'
        ))