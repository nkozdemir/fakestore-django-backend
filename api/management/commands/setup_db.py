from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

class Command(BaseCommand):
    help = 'Set up the entire database from scratch with FakeStore data and Django users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reset the database before setup',
        )

    def handle(self, *args, **options):
        force_reset = options.get('force', False)
        
        # Optionally reset the database
        if force_reset:
            self.stdout.write(self.style.WARNING('Force reset requested. Resetting database...'))
            self.reset_database()
        
        # Run migrations
        self.stdout.write(self.style.NOTICE('Applying migrations...'))
        call_command('migrate', verbosity=2)
        
        # Import all FakeStore data
        self.stdout.write(self.style.NOTICE('Importing all data from FakeStore API...'))
        call_command('import_all', verbosity=2)
        
        # Clean up any existing Django users (non-superusers)
        self.stdout.write(self.style.NOTICE('Cleaning up existing Django users...'))
        call_command('drop_django_users', verbosity=2)
        
        # Create Django users from FakeStore users
        self.stdout.write(self.style.NOTICE('Creating Django users from FakeStore users...'))
        call_command('create_django_users', verbosity=2)
        
        self.stdout.write(self.style.SUCCESS('Database setup completed successfully'))
        self.stdout.write(self.style.SUCCESS('All FakeStore data has been imported'))
        self.stdout.write(self.style.SUCCESS('Django users have been created for all FakeStore users'))
        self.stdout.write(self.style.SUCCESS('You can now run the server with: python manage.py runserver'))

    def reset_database(self):
        """Reset the database by dropping all tables and recreating them"""
        # Only works for PostgreSQL
        with connection.cursor() as cursor:
            # Disable foreign key checks
            cursor.execute("SET session_replication_role = 'replica';")
            
            # Get all tables in the current schema
            cursor.execute("""
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public'
                AND tablename != 'spatial_ref_sys';
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            # Drop all tables
            if tables:
                tables_str = ', '.join(f'"{table}"' for table in tables)
                cursor.execute(f'DROP TABLE IF EXISTS {tables_str} CASCADE;')
                self.stdout.write(self.style.SUCCESS(f'Dropped tables: {tables_str}'))
            
            # Re-enable foreign key checks
            cursor.execute("SET session_replication_role = 'origin';")
            
        self.stdout.write(self.style.SUCCESS('Database reset successfully'))
