import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from datetime import datetime
from employees.models import Employee
from sales.models import SaleInvoiceHeader, OfficialReceiptStatus, OfficialReceiptHeader
from commons.utils import parse_date


class Command(BaseCommand):
    help = "Insert official receipt headers from an Excel file."

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help="The Excel file (XLSX) containing official receipt headers.")

    def handle(self, *args, **options):
        filename = options['filename']

        # Load Excel file
        try:
            df = pd.read_excel(filename)
        except Exception as e:
            raise CommandError(f"Error reading file: {e}")

        # Check required columns
        required_columns = ['CODE', 'DATE',
                            'CREATOR', 'HEADER CODE', 'STATUS']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [
                col for col in required_columns if col not in df.columns]
            raise CommandError(f"Missing required columns: {
                               ', '.join(missing_columns)}")

        # Clean up data
        df['CODE'] = df['CODE'].fillna('').str.strip(
        ).str.upper().replace(" ", "-", regex=True)
        df['CREATOR'] = df['CREATOR'].fillna(
            '').str.strip().str.upper().replace(" ", "-", regex=True)
        df['HEADER CODE'] = df['HEADER CODE'].fillna(
            '').str.strip().str.upper().replace(" ", "-", regex=True)
        df['STATUS'] = df['STATUS'].fillna('').str.strip().str.upper()

        # Convert DATE column to datetime format
        try:
            df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce').dt.date
        except Exception:
            raise CommandError("Invalid date format detected. Use YYYY-MM-DD.")

        # Ensure no null dates exist after conversion
        if df['DATE'].isnull().any():
            raise CommandError(
                "Invalid or missing DATE values detected. Ensure all values are valid dates in YYYY-MM-DD format.")

        # Validate that CODE is unique in OfficialReceiptHeader
        existing_codes = set(OfficialReceiptHeader.objects.filter(
            code__in=df['CODE']).values_list('code', flat=True))
        duplicate_codes = set(df['CODE']) & existing_codes
        if duplicate_codes:
            raise CommandError(f"Duplicate CODE(s) found in database: {
                               ', '.join(duplicate_codes)}")

        # Validate that CREATOR exists in Employee
        creator_ids = set(df['CREATOR'])
        existing_creators = set(Employee.objects.filter(
            company_id__in=creator_ids).values_list('company_id', flat=True))
        missing_creators = creator_ids - existing_creators
        if missing_creators:
            raise CommandError(f"Invalid CREATOR(s) (company_id not found in Employee): {
                               ', '.join(missing_creators)}")

        # Validate that HEADER CODE exists in SaleInvoiceHeader
        header_codes = set(df['HEADER CODE'])
        existing_headers = set(SaleInvoiceHeader.objects.filter(
            code__in=header_codes).values_list('code', flat=True))
        missing_headers = header_codes - existing_headers
        if missing_headers:
            raise CommandError(f"Invalid HEADER CODE(s) (not found in SaleInvoiceHeader): {
                               ', '.join(missing_headers)}")

        # Validate that STATUS exists in OfficialReceiptStatus
        status_names = set(df['STATUS'])
        existing_statuses = set(OfficialReceiptStatus.objects.filter(
            name__in=status_names).values_list('name', flat=True))
        missing_statuses = status_names - existing_statuses
        if missing_statuses:
            raise CommandError(f"Invalid STATUS name(s) (not found in OfficialReceiptStatus): {
                               ', '.join(missing_statuses)}")

        # Insert records
        with transaction.atomic():
            for _, row in df.iterrows():
                code = row['CODE']
                date = row['DATE']
                creator = Employee.objects.get(company_id=row['CREATOR'])
                header = SaleInvoiceHeader.objects.get(
                    code=row['HEADER CODE'])
                status = OfficialReceiptStatus.objects.get(name=row['STATUS'])

                OfficialReceiptHeader.objects.create(
                    code=code,
                    date=date,
                    creator=creator,
                    sale_invoice_header=header,
                    status=status
                )

                self.stdout.write(self.style.SUCCESS(
                    f"Inserted: {code} - {date} - {creator.company_id}"))

        self.stdout.write(self.style.SUCCESS(
            "Purchase Receive Header data import completed!"))
