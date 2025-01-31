import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from customers.models import Customer, CustomerCategory


class Command(BaseCommand):
    help = 'Insert new customers from an Excel file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help='The Excel file (XLSX) containing customer data.'
        )

    def handle(self, *args, **options):
        filename = options['filename']

        # Load Excel file
        try:
            df = pd.read_excel(filename)
        except Exception as e:
            raise CommandError(f"Error reading file: {e}")

        # Check required columns
        required_columns = ['FIRST NAME', 'LAST NAME', 'CATEGORY']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [
                col for col in required_columns if col not in df.columns]
            raise CommandError(f"Missing required columns: {
                               ', '.join(missing_columns)}")

        # Clean up data
        df['FIRST NAME'] = df['FIRST NAME'].fillna('').str.strip()
        df['LAST NAME'] = df['LAST NAME'].fillna('').str.strip()
        df['MIDDLE NAME'] = df['MIDDLE NAME'].fillna('').str.strip()
        df['CATEGORY'] = df['CATEGORY'].fillna('').str.strip().str.upper()

        # Validate categories exist
        category_names = df['CATEGORY'].unique()
        existing_categories = set(CustomerCategory.objects.filter(
            name__in=category_names).values_list('name', flat=True))
        missing_categories = set(category_names) - existing_categories

        if missing_categories:
            raise CommandError(f"Categories not found: {
                               ', '.join(missing_categories)}")

        # Insert customers
        with transaction.atomic():
            for _, row in df.iterrows():
                first_name = row['FIRST NAME']
                last_name = row['LAST NAME']
                middle_name = row['MIDDLE NAME']
                category_name = row['CATEGORY']

                category = CustomerCategory.objects.get(name=category_name)

                # Avoid duplicate entries
                customer, created = Customer.objects.get_or_create(
                    first_name=first_name,
                    last_name=last_name,
                    category=category,
                    defaults={'middle_name': middle_name}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Inserted: {first_name} {last_name} ({category_name})"))
                else:
                    self.stdout.write(self.style.WARNING(f"Skipped (already exists): {
                                      first_name} {last_name} ({category_name})"))

        self.stdout.write(self.style.SUCCESS(
            "Customer data import completed!"))
