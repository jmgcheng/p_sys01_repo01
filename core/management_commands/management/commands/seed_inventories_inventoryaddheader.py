import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from inventories.models import InventoryAddHeader
from employees.models import Employee
from datetime import datetime
from commons.utils import parse_date


class Command(BaseCommand):
    help = 'Insert inventory add headers from an Excel file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help='The Excel file (XLSX) containing inventory add header data.'
        )

    def handle(self, *args, **options):
        filename = options['filename']

        # Load Excel file
        try:
            df = pd.read_excel(filename, dtype={'CODE': str, 'ADDER': str})
        except Exception as e:
            raise CommandError(f"Error reading file: {e}")

        # Check required columns
        required_columns = ['CODE', 'DATE', 'ADDER']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [
                col for col in required_columns if col not in df.columns]
            raise CommandError(f"Missing required columns: {
                               ', '.join(missing_columns)}")

        # Clean up data
        df['CODE'] = df['CODE'].fillna('').str.strip(
        ).str.upper().replace(" ", "-", regex=True)
        df['ADDER'] = df['ADDER'].fillna('').str.strip(
        ).str.upper().replace(" ", "-", regex=True)

        # Convert DATE column to datetime format
        try:
            df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
            df['DATE'] = df['DATE'].map(lambda x: x.strftime('%Y-%m-%d'))
        except Exception:
            raise CommandError("Invalid date format detected. Use YYYY-MM-DD.")

        # Ensure no null dates exist after conversion
        if df['DATE'].isnull().any():
            raise CommandError(
                "Invalid or missing DATE values detected. Ensure all values are valid dates in YYYY-MM-DD format.")

        # Validate unique codes
        existing_codes = set(
            InventoryAddHeader.objects.values_list('code', flat=True))
        duplicate_codes = set(df['CODE']) & existing_codes
        if duplicate_codes:
            raise CommandError(f"Duplicate CODE(s) already exist in database: {
                               ', '.join(duplicate_codes)}")

        # Validate that ADDER exists in Employee
        adder_ids = set(df['ADDER'].unique())
        existing_adders = set(Employee.objects.filter(
            company_id__in=adder_ids).values_list('company_id', flat=True))
        missing_adders = adder_ids - existing_adders

        if missing_adders:
            raise CommandError(f"Invalid ADDER(s) (company_id not found): {
                               ', '.join(missing_adders)}")

        # Insert records
        with transaction.atomic():
            for _, row in df.iterrows():
                code = row['CODE']
                date = parse_date(row.get('DATE'))  # Convert to date object
                adder = Employee.objects.get(company_id=row['ADDER'])

                # Create inventory record
                InventoryAddHeader.objects.create(
                    code=code,
                    date=date,
                    adder=adder
                )
                self.stdout.write(self.style.SUCCESS(
                    f"Inserted: {code} - {date} - {adder.company_id}"))

        self.stdout.write(self.style.SUCCESS(
            "Inventory data import completed!"))
