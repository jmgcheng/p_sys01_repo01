import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from inventories.models import InventoryDeductHeader
from employees.models import Employee
from datetime import datetime
from commons.utils import parse_date


class Command(BaseCommand):
    help = 'Insert inventory deduct headers from an Excel file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help='The Excel file (XLSX) containing inventory deduct header data.'
        )

    def handle(self, *args, **options):
        filename = options['filename']

        # Load Excel file
        try:
            df = pd.read_excel(filename)
        except Exception as e:
            raise CommandError(f"Error reading file: {e}")

        # Check required columns
        required_columns = ['CODE', 'DATE', 'DEDUCTER']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [
                col for col in required_columns if col not in df.columns]
            raise CommandError(f"Missing required columns: {
                               ', '.join(missing_columns)}")

        # Clean up data
        df['CODE'] = df['CODE'].fillna('').str.strip(
        ).str.upper().replace(" ", "-", regex=True)
        df['DEDUCTER'] = df['DEDUCTER'].fillna(
            '').str.strip().str.upper().replace(" ", "-", regex=True)

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
            InventoryDeductHeader.objects.values_list('code', flat=True))
        duplicate_codes = set(df['CODE']) & existing_codes
        if duplicate_codes:
            raise CommandError(f"Duplicate CODE(s) already exist in database: {
                               ', '.join(duplicate_codes)}")

        # Validate that ADDER exists in Employee
        deducter_ids = set(df['DEDUCTER'].unique())
        existing_deducters = set(Employee.objects.filter(
            company_id__in=deducter_ids).values_list('company_id', flat=True))
        missing_deducters = deducter_ids - existing_deducters

        if missing_deducters:
            raise CommandError(f"Invalid DEDUCTER(s) (company_id not found): {
                               ', '.join(missing_deducters)}")

        # Insert records
        with transaction.atomic():
            for _, row in df.iterrows():
                code = row['CODE']
                date = parse_date(row.get('DATE'))  # Convert to date object
                deducter = Employee.objects.get(company_id=row['DEDUCTER'])

                # Create inventory record
                InventoryDeductHeader.objects.create(
                    code=code,
                    date=date,
                    deducter=deducter
                )
                self.stdout.write(self.style.SUCCESS(
                    f"Inserted: {code} - {date} - {deducter.company_id}"))

        self.stdout.write(self.style.SUCCESS(
            "Inventory data import completed!"))
