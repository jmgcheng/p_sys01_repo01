import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from vendors.models import VendorCategory
from django.db import transaction


class Command(BaseCommand):
    help = 'Insert new vendor category from a CSV or XLSX file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help='The CSV or XLSX file containing vendor category to insert.')

    def handle(self, *args, **options):
        filename = options['filename']

        # Determine file type
        if filename.endswith('.csv'):
            df = pd.read_csv(filename)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filename)
        else:
            raise CommandError(
                'Unsupported file type. Please provide a CSV or XLSX file.')

        # Check if the required columns exist
        required_columns = ['NAME']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [
                col for col in required_columns if col not in df.columns]
            raise CommandError(f"Missing required columns: {
                               ', '.join(missing_columns)}")

        # Clean up data
        df['NAME'] = df['NAME'].fillna('').str.strip().str.upper()
        vendor_category = df['NAME'].dropna().unique()

        # Check for existing vendor_category
        existing_vendor_category = VendorCategory.objects.filter(
            name__in=vendor_category).values_list('name', flat=True)

        if existing_vendor_category:
            self.stdout.write(self.style.WARNING(
                'The following vendor category already exist in the database:'))
            for category in existing_vendor_category:
                self.stdout.write(f'- {category}')
            self.stdout.write(self.style.ERROR(
                'Aborting operation due to existing records.'))
        else:
            # Insert new vendor category in a transaction
            try:
                with transaction.atomic():
                    for _, row in df.iterrows():
                        name = row['NAME']

                        category = VendorCategory.objects.create(
                            name=name
                        )

                    self.stdout.write(self.style.SUCCESS(
                        'New vendor category records have been successfully added to the database.'))
            except Exception as e:
                raise CommandError(
                    f'Error inserting new vendor category: {str(e)}')
