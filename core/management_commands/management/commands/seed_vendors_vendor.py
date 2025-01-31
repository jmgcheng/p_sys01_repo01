import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from vendors.models import Vendor, VendorCategory


class Command(BaseCommand):
    help = 'Insert new vendors from an Excel file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help='The Excel file (XLSX) containing vendor data.'
        )

    def handle(self, *args, **options):
        filename = options['filename']

        # Load Excel file
        try:
            df = pd.read_excel(filename)
        except Exception as e:
            raise CommandError(f"Error reading file: {e}")

        # Check required columns
        required_columns = ['NAME', 'CATEGORY']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [
                col for col in required_columns if col not in df.columns]
            raise CommandError(f"Missing required columns: {
                               ', '.join(missing_columns)}")

        # Clean up data
        df['NAME'] = df['NAME'].fillna('').str.strip().str.upper()
        df['CATEGORY'] = df['CATEGORY'].fillna('').str.strip().str.upper()

        # Validate categories exist
        category_names = df['CATEGORY'].unique()
        existing_categories = set(VendorCategory.objects.filter(
            name__in=category_names).values_list('name', flat=True))
        missing_categories = set(category_names) - existing_categories

        if missing_categories:
            raise CommandError(f"Categories not found: {
                               ', '.join(missing_categories)}")

        # Insert vendors
        with transaction.atomic():
            for _, row in df.iterrows():
                name = row['NAME']
                category_name = row['CATEGORY']

                category = VendorCategory.objects.get(name=category_name)

                # Avoid duplicate entries
                vendor, created = Vendor.objects.get_or_create(
                    name=name,
                    category=category
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Inserted: {name} ({category_name})"))
                else:
                    self.stdout.write(self.style.WARNING(f"Skipped (already exists): {
                                      name} ({category_name})"))

        self.stdout.write(self.style.SUCCESS(
            "Vendor data import completed!"))
