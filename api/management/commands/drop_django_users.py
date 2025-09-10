from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Delete users (defaults to non-superusers only)'

    def add_arguments(self, parser):
        parser.add_argument('--include-superusers', action='store_true', default=False, help='Also delete superusers')

    def handle(self, *args, **options):
        User = get_user_model()
        qs = User.objects.all()
        # argparse stores --include-superusers as include_superusers
        include_supers = options.get('include_superusers', False)
        if not include_supers:
            qs = qs.filter(is_superuser=False)

        count = qs.count()
        qs.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} user(s).'))