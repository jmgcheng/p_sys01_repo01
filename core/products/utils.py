import pandas as pd
from django.db import transaction
from django.core.management.base import CommandError
from commons.utils import should_be
from products.models import ProductColor, ProductSize, ProductUnit, Product, ProductVariation


def load_foreign_keys():
    # just creating dictionaries here for easy access of values later
    colors = {c.name.upper(): c for c in ProductColor.objects.all()}
    sizes = {s.name.upper(): s for s in ProductSize.objects.all()}
    units = {u.name.upper(): u for u in ProductUnit.objects.all()}
    products = {p.name.upper(): p for p in Product.objects.all()}

    return {
        'colors': colors,
        'sizes': sizes,
        'units': units,
        'products': products,
    }


def verify_excel_products(df, mode='INSERT'):
    required_columns = ['PRODUCT CODE', 'NAME']

    if not all(col in df.columns for col in required_columns):
        missing_columns = [
            col for col in required_columns if col not in df.columns]
        raise CommandError(f"Missing required columns: {
                           ', '.join(missing_columns)}")

    df['PRODUCT CODE'] = df['PRODUCT CODE'].fillna('').astype(
        str).str.strip().str.upper().replace(" ", "-", regex=True)
    df['NAME'] = df['NAME'].fillna('').astype(str).str.strip()

    # Validate required columns should have values
    for col in required_columns:
        for _, row in df.iterrows():
            if row[col] == '':
                raise CommandError(f"Missing values in some {col} rows.")

    # check columns that should be unique
    columns_to_check = ['PRODUCT CODE']
    for column in columns_to_check:
        column_records = df[column].unique()
        field_name = 'name'
        if column == 'PRODUCT CODE':
            field_name = 'code'
    if mode == 'INSERT':
        should_be('NOT EXISTING', Product, 'Product',
                  field_name, column_records)
    elif mode == 'UPDATE':
        should_be('EXISTING', Product, 'Product', field_name, column_records)

    return df


def verify_excel_product_variations(df, mode='INSERT'):
    required_columns = ['PRODUCT VARIATION CODE',
                        'PRODUCT CODE', 'NAME', 'PRODUCT UNIT']

    df['PRODUCT SIZE'] = df['PRODUCT SIZE'].fillna('').astype(str).str.strip()

    if not all(col in df.columns for col in required_columns):
        missing_columns = [
            col for col in required_columns if col not in df.columns]
        raise CommandError(f"Missing required columns: {
                           ', '.join(missing_columns)}")

    # print(df)

    df['PRODUCT VARIATION CODE'] = df['PRODUCT VARIATION CODE'].fillna(
        '').astype(str).str.strip().str.upper().replace(" ", "-", regex=True)
    df['PRODUCT CODE'] = df['PRODUCT CODE'].fillna('').astype(
        str).str.strip().str.upper().replace(" ", "-", regex=True)
    df['NAME'] = df['NAME'].fillna('').astype(str).str.strip()
    df['PRODUCT UNIT'] = df['PRODUCT UNIT'].fillna('').str.strip().str.upper()

    # Validate required columns should have values
    for col in required_columns:
        for _, row in df.iterrows():
            if row[col] == '':
                raise CommandError(f"Missing values in some {col} rows.")

    # check columns that should be unique
    columns_to_check = ['PRODUCT VARIATION CODE']
    for column in columns_to_check:
        column_records = df[column].unique()
        field_name = 'name'
        if column == 'PRODUCT VARIATION CODE':
            field_name = 'code'
    if mode == 'INSERT':
        should_be('NOT EXISTING', ProductVariation, 'ProductVariation',
                  field_name, column_records)
    elif mode == 'UPDATE':
        should_be('EXISTING', ProductVariation,
                  'ProductVariation', field_name, column_records)

    # Verify if values exists
    columns_to_check = ['PRODUCT CODE', 'PRODUCT UNIT']
    for column in columns_to_check:
        column_records = df[column].unique()
        field_name = 'name'
        if column == 'PRODUCT CODE':
            model = Product
            model_name = 'Product'
            # field_name = 'code'
        elif column == 'PRODUCT UNIT':
            model = ProductUnit
            model_name = 'ProductUnit'

        should_be('EXISTING', model, model_name, field_name, column_records)

    # Verify value ONLY IF column is exisiting in file
    columns_to_check = ['PRODUCT SIZE', 'PRODUCT COLOR']
    for column in columns_to_check:
        if column in df.columns:
            #
            df[column] = df[column].replace({None: ''})
            df[column] = df[column].fillna('')
            df[column] = df[column].astype(str).str.strip().str.upper()
            df[column] = df[column].replace({'': None})

            #
            column_records = df[column].unique()
            column_records = column_records[~pd.isnull(column_records)]

            if not pd.isna(column_records).any():
                field_name = 'name'
                if column == 'PRODUCT SIZE':
                    model = ProductSize
                    model_name = 'ProductSize'
                elif column == 'PRODUCT COLOR':
                    model = ProductColor
                    model_name = 'ProductColor'

                should_be('EXISTING', model, model_name,
                          field_name, column_records)

    return df


def insert_excel_products(df):

    # First, verify and clean the input DataFrame
    df = verify_excel_products(df, 'INSERT')

    # Insert new products
    products = []

    for _, row in df.iterrows():

        # Create Product instance
        product = Product(
            code=row['PRODUCT CODE'],
            name=row['NAME'],
            excerpt='' if pd.isna(row.get('EXCERPT', None)
                                  ) else row.get('EXCERPT', None),
            description='' if pd.isna(
                row.get('DESCRIPTION', None)) else row.get('DESCRIPTION', None),
            image_url=''
        )

        products.append(product)

    with transaction.atomic():
        #
        Product.objects.bulk_create(products)

    return True


def insert_excel_product_variations(df):

    # First, verify and clean the input DataFrame
    df = verify_excel_product_variations(df, 'INSERT')

    # Load foreign key references
    foreign_keys = load_foreign_keys()

    #
    product_variations = []

    for _, row in df.iterrows():

        # Create Product Variation instance
        product_variation = ProductVariation(
            code=row['PRODUCT VARIATION CODE'],
            product=foreign_keys['products'].get(row['PRODUCT CODE'].upper()),
            name=row['NAME'],
            excerpt='' if pd.isna(row.get('EXCERPT', None)
                                  ) else row.get('EXCERPT', None),
            description='' if pd.isna(
                row.get('DESCRIPTION', None)) else row.get('DESCRIPTION', None),
            unit=None if pd.isna(foreign_keys['units'].get(
                row['PRODUCT UNIT'], None)) else foreign_keys['units'].get(row['PRODUCT UNIT'].upper(), None),
            size=None if pd.isna(foreign_keys['sizes'].get(
                row['PRODUCT SIZE'], None)) else foreign_keys['sizes'].get(row['PRODUCT SIZE'].upper(), None),
            color=None if pd.isna(foreign_keys['colors'].get(
                row['PRODUCT COLOR'], None)) else foreign_keys['colors'].get(row['PRODUCT COLOR'].upper(), None),
            image_url='',
        )
        product_variations.append(product_variation)

    with transaction.atomic():
        #
        ProductVariation.objects.bulk_create(product_variations)

    return True
