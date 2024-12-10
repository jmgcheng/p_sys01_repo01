import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from products.models import ProductColor
from django.db import transaction


class Command(BaseCommand):
    help = 'Insert new product color from a CSV or XLSX file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help='The CSV or XLSX file containing product color to insert.')

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
        product_color = df['NAME'].dropna().unique()

        # Check for existing product_color
        existing_product_color = ProductColor.objects.filter(
            name__in=product_color).values_list('name', flat=True)

        if existing_product_color:
            self.stdout.write(self.style.WARNING(
                'The following product color already exist in the database:'))
            for color in existing_product_color:
                self.stdout.write(f'- {color}')
            self.stdout.write(self.style.ERROR(
                'Aborting operation due to existing records.'))
        else:
            # Insert new product color in a transaction
            try:
                with transaction.atomic():
                    for _, row in df.iterrows():
                        name = row['NAME']

                        color = ProductColor.objects.create(
                            name=name
                        )

                    self.stdout.write(self.style.SUCCESS(
                        'New product color records have been successfully added to the database.'))
            except Exception as e:
                raise CommandError(
                    f'Error inserting new product color: {str(e)}')
