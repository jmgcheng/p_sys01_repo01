import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from sales.models import SaleInvoiceHeader, SaleInvoiceDetail
from products.models import ProductVariation


class Command(BaseCommand):
    help = "Insert sale invoice details from an Excel file."

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help="The Excel file (XLSX) containing sale invoice details.")

    def handle(self, *args, **options):
        filename = options['filename']

        # Load Excel file
        try:
            df = pd.read_excel(filename)
        except Exception as e:
            raise CommandError(f"Error reading file: {e}")

        # Check required columns
        required_columns = ['HEADER CODE',
                            'PRODUCT VARIATION CODE', 'QUANTITY']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [
                col for col in required_columns if col not in df.columns]
            raise CommandError(f"Missing required columns: {
                               ', '.join(missing_columns)}")

        # Clean up data
        df['HEADER CODE'] = df['HEADER CODE'].fillna(
            '').str.strip().str.upper().replace(" ", "-", regex=True)
        df['PRODUCT VARIATION CODE'] = df['PRODUCT VARIATION CODE'].fillna(
            '').str.strip().str.upper().replace(" ", "-", regex=True)

        # Ensure QUANTITY is numeric and positive
        if df['QUANTITY'].isnull().any() or (df['QUANTITY'] <= 0).any():
            raise CommandError("QUANTITY must be a positive integer.")

        # Validate that HEADER CODE exists in SaleInvoiceHeader
        header_codes = set(df['HEADER CODE'])
        existing_headers = set(SaleInvoiceHeader.objects.filter(
            code__in=header_codes).values_list('code', flat=True))
        missing_headers = header_codes - existing_headers

        if missing_headers:
            raise CommandError(f"Invalid HEADER CODE(s) (not found in SaleInvoiceHeader): {
                               ', '.join(missing_headers)}")

        # Validate that PRODUCT VARIATION CODE exists in ProductVariation
        variation_codes = set(df['PRODUCT VARIATION CODE'])
        existing_variations = set(ProductVariation.objects.filter(
            code__in=variation_codes).values_list('code', flat=True))
        missing_variations = variation_codes - existing_variations

        if missing_variations:
            raise CommandError(f"Invalid PRODUCT VARIATION CODE(s) (not found in ProductVariation): {
                               ', '.join(missing_variations)}")

        # Insert records
        with transaction.atomic():
            for _, row in df.iterrows():
                header = SaleInvoiceHeader.objects.get(
                    code=row['HEADER CODE'])
                variation = ProductVariation.objects.get(
                    code=row['PRODUCT VARIATION CODE'])
                quantity = int(row['QUANTITY'])

                SaleInvoiceDetail.objects.create(
                    sale_invoice_header=header,
                    product_variation=variation,
                    quantity_request=quantity
                )

                self.stdout.write(self.style.SUCCESS(
                    f"Inserted: {header.code} - {variation.code} - {quantity}"))

        self.stdout.write(self.style.SUCCESS(
            "sale invoice Details data import completed!"))
