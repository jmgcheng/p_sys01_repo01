import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from products.models import ProductUnit
from django.db import transaction


class Command(BaseCommand):
    help = 'Insert new product unit from a CSV or XLSX file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help='The CSV or XLSX file containing product unit to insert.')

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
        df['NAME'] = df['NAME'].fillna('').astype(str).str.strip().str.upper()
        product_unit = df['NAME'].dropna().unique()

        # Check for existing product_unit
        existing_product_unit = ProductUnit.objects.filter(
            name__in=product_unit).values_list('name', flat=True)

        if existing_product_unit:
            self.stdout.write(self.style.WARNING(
                'The following product unit already exist in the database:'))
            for size in existing_product_unit:
                self.stdout.write(f'- {size}')
            self.stdout.write(self.style.ERROR(
                'Aborting operation due to existing records.'))
        else:
            # Insert new product unit in a transaction
            try:
                with transaction.atomic():
                    for _, row in df.iterrows():
                        name = row['NAME']

                        size = ProductUnit.objects.create(
                            name=name
                        )

                    self.stdout.write(self.style.SUCCESS(
                        'New product unit records have been successfully added to the database.'))
            except Exception as e:
                raise CommandError(
                    f'Error inserting new product unit: {str(e)}')
