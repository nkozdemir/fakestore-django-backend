from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
import subprocess
import os

class Command(BaseCommand):
    help = 'Set up the entire database from scratch with FakeStore data and Django users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reset the database before setup',
        )
        parser.add_argument(
            '--with-docker',
            action='store_true',
            help='Start Docker services (PostgreSQL and Redis)',
        )

    def handle(self, *args, **options):
        # 1) migrations
        call_command('migrate', interactive=False, verbosity=1)

        # 2) optional clean (drop users first to avoid FK cascades later)
        self.stdout.write('Cleaning up existing Django users...')
        call_command('drop_django_users', verbosity=1)

        # 3) import data fresh
        self.stdout.write('Importing all data from FakeStore API...')
        call_command('import_products', verbosity=1)
        call_command('import_users', verbosity=1)
        call_command('import_carts', verbosity=1)

        # 4) ensure passwords
        self.stdout.write('Ensuring passwords for users...')
        call_command('create_django_users', verbosity=1)

        self.stdout.write(self.style.SUCCESS('Database setup completed.'))

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
        
    def start_docker_services(self):
        """Start Docker services (PostgreSQL and Redis)"""
        try:
            # Get the directory containing manage.py
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            
            # Run docker-compose up -d
            subprocess.run(['docker-compose', 'up', '-d'], cwd=base_dir, check=True)
            self.stdout.write(self.style.SUCCESS('Docker services started successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to start Docker services: {str(e)}'))
