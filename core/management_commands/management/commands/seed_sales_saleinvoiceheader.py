import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from employees.models import Employee
from customers.models import Customer
from sales.models import SaleInvoiceStatus, SaleInvoiceHeader, SaleInvoiceCategory
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
        required_columns = ['CODE', 'DATE', 'CATEGORY',
                            'CREATOR', 'CUSTOMER', 'STATUS']
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
        df['CUSTOMER'] = df['CUSTOMER'].fillna('').astype(
            str).str.strip().str.upper().replace(" ", "-", regex=True)
        df['CATEGORY'] = df['CATEGORY'].fillna('').str.strip().str.upper()
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
            SaleInvoiceHeader.objects.values_list('code', flat=True))
        duplicate_codes = set(df['CODE']) & existing_codes
        if duplicate_codes:
            raise CommandError(f"Duplicate CODE(s) already exist in database: {
                               ', '.join(duplicate_codes)}")

        # Validate that CREATOR exists in Employee
        creator_ids = set(df['CREATOR'].unique())
        existing_creator = set(Employee.objects.filter(
            company_id__in=creator_ids).values_list('company_id', flat=True))
        missing_creator = creator_ids - existing_creator
        if missing_creator:
            raise CommandError(f"Invalid CREATOR(s) (company_id not found): {
                               ', '.join(missing_creator)}")

        # Validate that CUSTOMER exists in Customer
        customer_ids = list(df['CUSTOMER'].unique())
        customer_ids = set([x for x in customer_ids if x.strip()])

        existing_customer = set(Customer.objects.filter(
            customer_id__in=customer_ids).values_list('customer_id', flat=True))
        missing_customer = customer_ids - existing_customer
        if missing_customer:
            raise CommandError(f"Invalid CUSTOMER(s) (customer_id not found): {
                               ', '.join(missing_customer)}")

        # Validate that CATEGORY exists in SaleInvoiceCategory
        category_names = df['CATEGORY'].unique()
        existing_category = set(SaleInvoiceCategory.objects.filter(
            name__in=category_names).values_list('name', flat=True))
        missing_category = set(category_names) - existing_category
        if missing_category:
            raise CommandError(f"Category not found: {
                               ', '.join(missing_category)}")

        # Validate that STATUS exists in SaleInvoiceStatus
        status_names = df['STATUS'].unique()
        existing_status = set(SaleInvoiceStatus.objects.filter(
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
                category = SaleInvoiceCategory.objects.get(
                    name=row['CATEGORY'])
                creator = Employee.objects.get(company_id=row['CREATOR'])

                # Handle optional CUSTOMER field
                customer = None
                if row['CUSTOMER']:
                    customer = Customer.objects.get(
                        customer_id=row['CUSTOMER'])

                status = SaleInvoiceStatus.objects.get(name=row['STATUS'])

                # Create  record
                SaleInvoiceHeader.objects.create(
                    code=code,
                    date=date,
                    category=category,
                    creator=creator,
                    status=status,
                    customer=customer
                )
                self.stdout.write(self.style.SUCCESS(
                    f"Inserted: {code} - {date}"))

        self.stdout.write(self.style.SUCCESS(
            "Sale Invoice Header data import completed!"))
