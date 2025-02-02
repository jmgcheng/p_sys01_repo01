from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import timedelta, date
import random
from random import randint
import pandas as pd
import os


class Command(BaseCommand):
    help = "Generate dummy transactions for inventory system"

    def handle(self, *args, **kwargs):
        self.setup_defaults()
        self.main_loop()
        self.export_excel()

    def setup_defaults(self):
        self.start_loop_date = date(2025, 1, 1)
        self.end_loop_date = date(2025, 2, 1)
        self.current_date = self.start_loop_date
        self.product_variation_list = [
            {'code': 'PV-001', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-002', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-003', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
        ]
        self.todays_request_product_variations = []
        self.purchase_request_header_list = []
        self.purchase_request_detail_list = []
        self.purchase_receive_header_list = []
        self.purchase_receive_detail_list = []
        self.sale_invoice_header_list = []
        self.sale_invoice_detail_list = []
        self.official_receipt_header_list = []
        self.official_receipt_detail_list = []
        self.purchase_requestor_list = ['TEST-ID-14', 'TEST-ID-15']
        self.purchase_approver_list = ['TEST-ID-14', 'TEST-ID-15']
        self.sale_representative_list = ['TEST-ID-14', 'TEST-ID-15']
        self.vendor_list = ['VENDOR-01', 'VENDOR-02']
        self.customer_list = ['CUST-01', 'CUST-02', 'CUST-03']
        self.sale_category_list = ['RETAIL', 'PATIENT',
                                   'WHOLESALE', 'GOVERNMENT', 'CORPORATE']

    def create_purchase_request_header(self):
        request_header_dict = {
            'code': f'P-REQ-{len(self.purchase_request_header_list) + 1}',
            'date': self.current_date,
            'requestor': random.choice(self.purchase_requestor_list),
            'approver': random.choice(self.purchase_approver_list),
            'vendor': random.choice(self.vendor_list),
            'status': 'OPEN (PURCHASING)',
        }

        return request_header_dict

    def create_purchase_request_detail(self, purchase_request_header):
        detail_list = []

        for product_variation in self.todays_request_product_variations:
            detail_dict = {
                'purchase_request_header': purchase_request_header['code'],
                'product_variation': product_variation['code'],
                'quantity_request': product_variation['quantity_alert']
            }

            detail_list.append(detail_dict)

        return detail_list

    def create_purchase_request_transactions(self):
        # filter if really need to request
        for purchase_request_header in self.purchase_request_header_list:
            if purchase_request_header['status'] == 'OPEN (PURCHASING)':
                for purchase_request_detail in self.purchase_request_detail_list:
                    if purchase_request_detail['purchase_request_header'] == purchase_request_header['code']:
                        for product_variation in self.product_variation_list:
                            if product_variation['code'] == purchase_request_detail['product_variation']:
                                for todays_request_product_variation in self.todays_request_product_variations:
                                    if todays_request_product_variation['code'] == product_variation['code']:
                                        if todays_request_product_variation['quantity_alert'] >= (product_variation['current_quantity'] + product_variation['arriving_quantity']):
                                            self.todays_request_product_variations.remove(
                                                todays_request_product_variation)

        #
        if len(self.todays_request_product_variations) > 0:
            print('requesting...')
            #
            purchase_request_header = self.create_purchase_request_header()
            self.purchase_request_header_list.append(purchase_request_header)
            #
            purchase_request_details = self.create_purchase_request_detail(
                purchase_request_header)
            for x in purchase_request_details:
                self.purchase_request_detail_list.append(x)

    def update_product_variant_arriving_quantity(self):
        for purchase_request_header in self.purchase_request_header_list:
            if purchase_request_header['status'] == 'OPEN (PURCHASING)':
                for purchase_request_detail in self.purchase_request_detail_list:
                    if purchase_request_detail['purchase_request_header'] == purchase_request_header['code']:
                        for product_variation in self.product_variation_list:
                            if product_variation['code'] == purchase_request_detail['product_variation']:
                                product_variation['arriving_quantity'] = product_variation['arriving_quantity'] + \
                                    purchase_request_detail['quantity_request']

    def reset_product_variant_arriving_quantity(self):
        for product_variation in self.product_variation_list:
            product_variation['arriving_quantity'] = 0

    def create_purchase_receive_header(self, purchase_request_header):
        receive_header_dict = {
            'code': f'P-REC-{len(self.purchase_receive_header_list) + 1}',
            'date': self.current_date,
            'receiver': random.choice(self.purchase_requestor_list),
            'purchase_request_header': purchase_request_header['code'],
            'status': 'CLOSED',
        }

        return receive_header_dict

    def create_purchase_receive_detail(self, purchase_request_header, purchase_receive_header):
        detail_list = []

        for purchase_request_detail in self.purchase_request_detail_list:
            if purchase_request_detail['purchase_request_header'] == purchase_request_header['code']:
                detail_dict = {
                    'purchase_receive_header': purchase_receive_header['code'],
                    'product_variation': purchase_request_detail['product_variation'],
                    'quantity_received': purchase_request_detail['quantity_request']
                }

                detail_list.append(detail_dict)

        return detail_list

    def create_purchase_receive_transactions(self):
        #
        pending_request_transactions = []

        #
        for purchase_request_header in self.purchase_request_header_list:
            if purchase_request_header['status'] == 'OPEN (PURCHASING)':
                print('receiving...')

                #
                purchase_receive_header = self.create_purchase_receive_header(
                    purchase_request_header)
                self.purchase_receive_header_list.append(
                    purchase_receive_header)

                #
                purchase_receive_details = self.create_purchase_receive_detail(
                    purchase_request_header, purchase_receive_header)
                for purchase_receive_detail in purchase_receive_details:
                    self.purchase_receive_detail_list.append(
                        purchase_receive_detail)

                #
                for purchase_receive_detail in purchase_receive_details:
                    for product_variation in self.product_variation_list:
                        if product_variation['code'] == purchase_receive_detail['product_variation']:
                            product_variation['current_quantity'] = product_variation['current_quantity'] + \
                                purchase_receive_detail['quantity_received']
                            product_variation['arriving_quantity'] = product_variation['arriving_quantity'] - \
                                purchase_receive_detail['quantity_received']

                #
                purchase_request_header['status'] = 'CLOSED'

    def create_sale_invoice_header(self):
        sale_header_dict = {
            'code': f'SI-{len(self.sale_invoice_header_list) + 1}',
            'date': self.current_date,
            'category': random.choice(self.sale_category_list),
            'creator': random.choice(self.sale_representative_list),
            'customer': random.choice(self.customer_list),
            'status': 'OPEN (FOR PAYMENT)'
        }

        return sale_header_dict

    def create_sale_invoice_detail(self, sale_invoice_header):
        detail_list = []
        num_of_items_sold = randint(1, 3)

        for x in range(1, num_of_items_sold + 1):
            product_variation = random.choice(self.product_variation_list)
            detail_dict = {
                'sale_invoice_header': sale_invoice_header['code'],
                'product_variation': product_variation['code'],
                'quantity_request': randint(1, 20)
            }

            detail_list.append(detail_dict)

        return detail_list

    def create_sale_invoice_transactions(self):
        #
        sale_invoice_header = self.create_sale_invoice_header()
        self.sale_invoice_header_list.append(sale_invoice_header)
        #
        sale_invoice_details = self.create_sale_invoice_detail(
            sale_invoice_header)
        for x in sale_invoice_details:
            self.sale_invoice_detail_list.append(x)

    def create_official_receipt_header(self, sale_invoice_header):
        receipt_header_dict = {
            'code': f'OR-{len(self.official_receipt_header_list) + 1}',
            'date': self.current_date,
            'creator': random.choice(self.sale_representative_list),
            'sale_invoice_header': sale_invoice_header['code'],
            'status': 'PAID',
        }

        return receipt_header_dict

    def create_official_receipt_detail(self, sale_invoice_header, official_receipt_header):
        detail_list = []

        for sale_invoice_detail in self.sale_invoice_detail_list:
            if sale_invoice_detail['sale_invoice_header'] == sale_invoice_header['code']:
                detail_dict = {
                    'official_receipt_header': official_receipt_header['code'],
                    'product_variation': sale_invoice_detail['product_variation'],
                    'quantity_paid': sale_invoice_detail['quantity_request']
                }

                detail_list.append(detail_dict)

        return detail_list

    def create_official_receipt_transactions(self):
        #
        for sale_invoice_header in self.sale_invoice_header_list:
            if sale_invoice_header['status'] == 'OPEN (FOR PAYMENT)':
                print('releasing...')

                #
                official_receipt_header = self.create_official_receipt_header(
                    sale_invoice_header)
                self.official_receipt_header_list.append(
                    official_receipt_header)

                #
                official_receipt_details = self.create_official_receipt_detail(
                    sale_invoice_header, official_receipt_header)
                for official_receipt_detail in official_receipt_details:
                    self.official_receipt_detail_list.append(
                        official_receipt_detail)

                #
                for official_receipt_detail in official_receipt_details:
                    for product_variation in self.product_variation_list:
                        if product_variation['code'] == official_receipt_detail['product_variation']:
                            product_variation['current_quantity'] = product_variation['current_quantity'] - \
                                official_receipt_detail['quantity_paid']

                #
                sale_invoice_header['status'] = 'CLOSED'

    def main_loop(self):
        while self.current_date <= self.end_loop_date:
            print(f'Today is: {self.current_date}')

            #
            self.todays_request_product_variations = [product_variation for product_variation in self.product_variation_list if (
                product_variation['current_quantity'] + product_variation['arriving_quantity']) < product_variation['quantity_alert']]

            #
            self.create_purchase_request_transactions()
            self.update_product_variant_arriving_quantity()
            #
            self.create_purchase_receive_transactions()

            #
            self.create_sale_invoice_transactions()
            #
            self.create_official_receipt_transactions()

            #
            self.reset_product_variant_arriving_quantity()
            self.current_date += timedelta(days=1)

    def export_excel(self):
        output_dir = os.path.join(os.getcwd())
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "dummy_transactions.xlsx")

        with pd.ExcelWriter(file_path) as writer:
            pd.DataFrame(self.purchase_request_header_list).to_excel(
                writer, sheet_name="Purchase Requests", index=False)
            pd.DataFrame(self.purchase_request_detail_list).to_excel(
                writer, sheet_name="Request Details", index=False)
            pd.DataFrame(self.purchase_receive_header_list).to_excel(
                writer, sheet_name="Purchase Receives", index=False)
            pd.DataFrame(self.purchase_receive_detail_list).to_excel(
                writer, sheet_name="Receive Details", index=False)
            pd.DataFrame(self.sale_invoice_header_list).to_excel(
                writer, sheet_name="Sale Invoices", index=False)
            pd.DataFrame(self.sale_invoice_detail_list).to_excel(
                writer, sheet_name="Invoice Details", index=False)
            pd.DataFrame(self.official_receipt_header_list).to_excel(
                writer, sheet_name="Official Receipts", index=False)
            pd.DataFrame(self.official_receipt_detail_list).to_excel(
                writer, sheet_name="Receipt Details", index=False)

        self.stdout.write(self.style.SUCCESS(
            f"Dummy transactions saved to {file_path}"))
