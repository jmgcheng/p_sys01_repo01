import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from sales.models import SaleInvoiceStatus
from django.db import transaction


class Command(BaseCommand):
    help = 'Insert new sale invoice status from a CSV or XLSX file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help='The CSV or XLSX file containing sale invoice status to insert.')

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
        status_name = df['NAME'].dropna().unique()

        # Check for existing status_name
        existing_status_name = SaleInvoiceStatus.objects.filter(
            name__in=status_name).values_list('name', flat=True)

        if existing_status_name:
            self.stdout.write(self.style.WARNING(
                'The following sale invoice status already exist in the database:'))
            for category in existing_status_name:
                self.stdout.write(f'- {category}')
            self.stdout.write(self.style.ERROR(
                'Aborting operation due to existing records.'))
        else:
            # Insert new sale invoice status in a transaction
            try:
                with transaction.atomic():
                    for _, row in df.iterrows():
                        name = row['NAME']

                        category = SaleInvoiceStatus.objects.create(
                            name=name
                        )

                    self.stdout.write(self.style.SUCCESS(
                        'New sale invoice status records have been successfully added to the database.'))
            except Exception as e:
                raise CommandError(
                    f'Error inserting new sale invoice status: {str(e)}')
