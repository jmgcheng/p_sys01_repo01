import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from employees.models import Employee
from vendors.models import Vendor
from purchases.models import PurchaseRequestStatus, PurchaseRequestHeader
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
            df = pd.read_excel(filename)
        except Exception as e:
            raise CommandError(f"Error reading file: {e}")

        # Check required columns
        required_columns = ['CODE', 'DATE',
                            'REQUESTOR', 'APPROVER', 'VENDOR', 'STATUS']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [
                col for col in required_columns if col not in df.columns]
            raise CommandError(f"Missing required columns: {
                               ', '.join(missing_columns)}")

        # Clean up data
        df['CODE'] = df['CODE'].fillna('').str.strip(
        ).str.upper().replace(" ", "-", regex=True)
        df['REQUESTOR'] = df['REQUESTOR'].fillna(
            '').str.strip().str.upper().replace(" ", "-", regex=True)
        df['APPROVER'] = df['APPROVER'].fillna(
            '').str.strip().str.upper().replace(" ", "-", regex=True)
        df['VENDOR'] = df['VENDOR'].fillna('').str.strip().str.upper()
        df['STATUS'] = df['STATUS'].fillna('').str.strip().str.upper()

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
            PurchaseRequestHeader.objects.values_list('code', flat=True))
        duplicate_codes = set(df['CODE']) & existing_codes
        if duplicate_codes:
            raise CommandError(f"Duplicate CODE(s) already exist in database: {
                               ', '.join(duplicate_codes)}")

        # need improvement. keeps hitting db
        # Validate that REQUESTOR exists in Employee
        requestor_ids = set(df['REQUESTOR'].unique())
        existing_requestor = set(Employee.objects.filter(
            company_id__in=requestor_ids).values_list('company_id', flat=True))
        missing_requestor = requestor_ids - existing_requestor
        if missing_requestor:
            raise CommandError(f"Invalid REQUESTOR(s) (company_id not found): {
                               ', '.join(missing_requestor)}")

        # Validate that APPROVER exists in Employee
        approver_ids = set(df['APPROVER'].unique())
        existing_approver = set(Employee.objects.filter(
            company_id__in=approver_ids).values_list('company_id', flat=True))
        missing_approver = approver_ids - existing_approver
        if missing_approver:
            raise CommandError(f"Invalid APPROVER(s) (company_id not found): {
                               ', '.join(missing_approver)}")

        # Validate that VENDOR exists in Vendor
        vendor_names = set(df['VENDOR'].unique())
        existing_vendor = set(Vendor.objects.filter(
            name__in=vendor_names).values_list('name', flat=True))
        missing_vendor = vendor_names - existing_vendor
        if missing_vendor:
            raise CommandError(f"Invalid VENDOR(s) (name not found): {
                               ', '.join(missing_vendor)}")

        # Validate that STATUS exists in PurchaseRequestStatus
        status_names = df['STATUS'].unique()
        existing_status = set(PurchaseRequestStatus.objects.filter(
            name__in=status_names).values_list('name', flat=True))
        missing_status = set(status_names) - existing_status
        if missing_status:
            raise CommandError(f"Status not found: {
                               ', '.join(missing_status)}")

        # Insert records
        with transaction.atomic():
            for _, row in df.iterrows():
                code = row['CODE']
                date = parse_date(row.get('DATE'))  # Convert to date object
                requestor = Employee.objects.get(company_id=row['REQUESTOR'])
                approver = Employee.objects.get(company_id=row['APPROVER'])
                vendor = Vendor.objects.get(name=row['VENDOR'])
                status = PurchaseRequestStatus.objects.get(name=row['STATUS'])

                # Create  record
                PurchaseRequestHeader.objects.create(
                    code=code,
                    date=date,
                    requestor=requestor,
                    approver=approver,
                    vendor=vendor,
                    status=status
                )
                self.stdout.write(self.style.SUCCESS(
                    f"Inserted: {code} - {date}"))

        self.stdout.write(self.style.SUCCESS(
            "Purchase Request Header data import completed!"))
