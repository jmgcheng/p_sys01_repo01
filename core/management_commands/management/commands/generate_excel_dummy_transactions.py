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
        self.end_loop_date = date(2025, 12, 30)
        self.current_date = self.start_loop_date
        self.product_variation_list = [
            {'code': 'PV-001', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-002', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-003', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-004', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-005', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-006', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-007', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-008', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-009', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-010', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-011', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-012', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-013', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-014', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-015', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-016', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-017', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-018', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-019', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-020', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-021', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-022', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-023', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-024', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-025', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-026', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-027', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-028', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-029', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-030', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-031', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-032', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-033', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-034', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-035', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-036', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-037', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-038', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-039', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-040', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-041', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-042', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-043', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-044', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-045', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-046', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-047', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-048', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-049', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-050', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'code': 'PV-051', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'code': 'PV-052', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'code': 'PV-053', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'code': 'PV-054', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'code': 'PV-055', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'code': 'PV-056', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'code': 'PV-057', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-058', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-059', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-060', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-061', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-062', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-063', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-064', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-065', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-066', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-067', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-068', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-069', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-070', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-071', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-072', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-073', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-074', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-075', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-076', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-077', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-078', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-079', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-080', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'code': 'PV-081', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-082', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-083', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'code': 'PV-084', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-085', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-086', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-087', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-088', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-089', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-090', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-091', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-092', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-093', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-094', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-095', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-096', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-097', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-098', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-099', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-100', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'code': 'PV-101', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
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
        self.purchase_requestor_list = ['EMP-ID-25', 'EMP-ID-26', 'EMP-ID-27']
        self.purchase_approver_list = [
            'EMP-ID-27', 'EMP-ID-20', 'EMP-ID-21', 'EMP-ID-22', 'EMP-ID-23', 'EMP-ID-24']
        self.sale_representative_list = [
            'EMP-ID-28', 'EMP-ID-29', 'EMP-ID-30', 'EMP-ID-31', 'EMP-ID-32']
        self.vendor_list = ['VENDOR-01', 'VENDOR-02', 'VENDOR-03',
                            'VENDOR-04', 'VENDOR-05', 'VENDOR-06', 'VENDOR-07']
        self.customer_list = ['CUST-ID-01', 'CUST-ID-02', 'CUST-ID-03', 'CUST-ID-04', 'CUST-ID-05', 'CUST-ID-06', 'CUST-ID-07', 'CUST-ID-08', 'CUST-ID-09', 'CUST-ID-10', 'CUST-ID-11', 'CUST-ID-12', 'CUST-ID-13', 'CUST-ID-14',
                              'CUST-ID-15', 'CUST-ID-16', 'CUST-ID-17', 'CUST-ID-18', 'CUST-ID-19', 'CUST-ID-20', 'CUST-ID-21', 'CUST-ID-22', 'CUST-ID-23', 'CUST-ID-24', 'CUST-ID-25', 'CUST-ID-26', 'CUST-ID-27', 'CUST-ID-28', 'CUST-ID-29', 'CUST-ID-30']
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

                # create random issue in quantity_received to simulate real life
                quantity_received = 0
                issue_is = randint(1, 10)
                if issue_is <= 2:  # 35% chance of issue
                    print('created issue in purchase receive detail')
                    quantity_received = randint(
                        purchase_request_detail['quantity_request'] - 90, purchase_request_detail['quantity_request'] + 100)
                else:
                    quantity_received = purchase_request_detail['quantity_request']

                detail_dict = {
                    'purchase_receive_header': purchase_receive_header['code'],
                    'product_variation': purchase_request_detail['product_variation'],
                    'quantity_received': quantity_received
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
        num_of_items_sold = randint(1, 5)

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
                # create random issue in quantity_paid to simulate real life
                quantity_paid = 0
                issue_is = randint(1, 10)
                if issue_is <= 1:  # 10% chance of issue
                    print('created issue in official receipt detail')
                    quantity_paid = randint(
                        sale_invoice_detail['quantity_request'] - 10, sale_invoice_detail['quantity_request'] + 20)
                else:
                    quantity_paid = sale_invoice_detail['quantity_request']

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

            # add random customer transaction
            num_customer_today = randint(5, 10)
            for x in range(1, num_customer_today + 1):
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
