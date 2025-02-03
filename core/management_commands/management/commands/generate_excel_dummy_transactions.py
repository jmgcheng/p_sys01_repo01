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
        self.end_loop_date = date(2025, 12, 31)
        self.current_date = self.start_loop_date
        self.product_variation_list = [
            {'CODE': 'PV-001', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-002', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-003', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-004', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-005', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-006', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-007', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-008', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-009', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-010', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-011', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-012', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-013', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-014', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-015', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-016', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-017', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-018', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-019', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-020', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-021', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-022', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-023', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-024', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-025', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-026', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-027', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-028', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-029', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-030', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-031', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-032', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-033', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-034', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-035', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-036', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-037', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-038', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-039', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-040', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-041', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-042', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-043', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-044', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-045', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-046', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-047', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-048', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-049', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-050', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'CODE': 'PV-051', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'CODE': 'PV-052', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'CODE': 'PV-053', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'CODE': 'PV-054', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'CODE': 'PV-055', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'CODE': 'PV-056', 'current_quantity': 0,
                'quantity_alert': 200, 'arriving_quantity': 0},
            {'CODE': 'PV-057', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-058', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-059', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-060', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-061', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-062', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-063', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-064', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-065', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-066', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-067', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-068', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-069', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-070', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-071', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-072', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-073', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-074', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-075', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-076', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-077', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-078', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-079', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-080', 'current_quantity': 0,
                'quantity_alert': 100, 'arriving_quantity': 0},
            {'CODE': 'PV-081', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-082', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-083', 'current_quantity': 0,
                'quantity_alert': 300, 'arriving_quantity': 0},
            {'CODE': 'PV-084', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-085', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-086', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-087', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-088', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-089', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-090', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-091', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-092', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-093', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-094', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-095', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-096', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-097', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-098', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-099', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-100', 'current_quantity': 0,
                'quantity_alert': 500, 'arriving_quantity': 0},
            {'CODE': 'PV-101', 'current_quantity': 0,
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
            'CODE': f'P-REQ-{len(self.purchase_request_header_list) + 1}',
            'DATE': self.current_date,
            'REQUESTOR': random.choice(self.purchase_requestor_list),
            'APPROVER': random.choice(self.purchase_approver_list),
            'VENDOR': random.choice(self.vendor_list),
            'STATUS': 'OPEN (PURCHASING)',
        }

        return request_header_dict

    def create_purchase_request_detail(self, purchase_request_header):
        detail_list = []

        for product_variation in self.todays_request_product_variations:
            detail_dict = {
                'HEADER CODE': purchase_request_header['CODE'],
                'PRODUCT VARIATION CODE': product_variation['CODE'],
                'QUANTITY': product_variation['quantity_alert']
            }

            detail_list.append(detail_dict)

        return detail_list

    def create_purchase_request_transactions(self):
        # filter if really need to request
        for purchase_request_header in self.purchase_request_header_list:
            if purchase_request_header['STATUS'] == 'OPEN (PURCHASING)':
                for purchase_request_detail in self.purchase_request_detail_list:
                    if purchase_request_detail['HEADER CODE'] == purchase_request_header['CODE']:
                        for product_variation in self.product_variation_list:
                            if product_variation['CODE'] == purchase_request_detail['PRODUCT VARIATION CODE']:
                                for todays_request_product_variation in self.todays_request_product_variations:
                                    if todays_request_product_variation['CODE'] == product_variation['CODE']:
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
            if purchase_request_header['STATUS'] == 'OPEN (PURCHASING)':
                for purchase_request_detail in self.purchase_request_detail_list:
                    if purchase_request_detail['HEADER CODE'] == purchase_request_header['CODE']:
                        for product_variation in self.product_variation_list:
                            if product_variation['CODE'] == purchase_request_detail['PRODUCT VARIATION CODE']:
                                product_variation['arriving_quantity'] = product_variation['arriving_quantity'] + \
                                    purchase_request_detail['QUANTITY']

    def reset_product_variant_arriving_quantity(self):
        for product_variation in self.product_variation_list:
            product_variation['arriving_quantity'] = 0

    def create_purchase_receive_header(self, purchase_request_header):
        receive_header_dict = {
            'CODE': f'P-REC-{len(self.purchase_receive_header_list) + 1}',
            'DATE': self.current_date,
            'RECEIVER': random.choice(self.purchase_requestor_list),
            'HEADER CODE': purchase_request_header['CODE'],
            'STATUS': 'CLOSED',
        }

        return receive_header_dict

    def create_purchase_receive_detail(self, purchase_request_header, purchase_receive_header):
        detail_list = []

        for purchase_request_detail in self.purchase_request_detail_list:
            if purchase_request_detail['HEADER CODE'] == purchase_request_header['CODE']:

                # create random issue in quantity_received to simulate real life
                quantity_received = 0
                issue_is = randint(1, 10)
                if issue_is <= 2:  # 35% chance of issue
                    print('created issue in purchase receive detail')
                    quantity_received = randint(
                        purchase_request_detail['QUANTITY'] - 90, purchase_request_detail['QUANTITY'] + 100)
                else:
                    quantity_received = purchase_request_detail['QUANTITY']

                detail_dict = {
                    'HEADER CODE': purchase_receive_header['CODE'],
                    'PRODUCT VARIATION CODE': purchase_request_detail['PRODUCT VARIATION CODE'],
                    'QUANTITY': quantity_received
                }

                detail_list.append(detail_dict)

        return detail_list

    def create_purchase_receive_transactions(self):
        #
        pending_request_transactions = []

        #
        for purchase_request_header in self.purchase_request_header_list:
            if purchase_request_header['STATUS'] == 'OPEN (PURCHASING)':
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
                        if product_variation['CODE'] == purchase_receive_detail['PRODUCT VARIATION CODE']:
                            product_variation['current_quantity'] = product_variation['current_quantity'] + \
                                purchase_receive_detail['QUANTITY']
                            product_variation['arriving_quantity'] = product_variation['arriving_quantity'] - \
                                purchase_receive_detail['QUANTITY']

                #
                purchase_request_header['STATUS'] = 'CLOSED'

    def create_sale_invoice_header(self):
        sale_header_dict = {
            'CODE': f'SI-{len(self.sale_invoice_header_list) + 1}',
            'DATE': self.current_date,
            'CATEGORY': random.choice(self.sale_category_list),
            'CREATOR': random.choice(self.sale_representative_list),
            'CUSTOMER': random.choice(self.customer_list),
            'STATUS': 'OPEN (FOR PAYMENT)'
        }

        return sale_header_dict

    def create_sale_invoice_detail(self, sale_invoice_header):
        detail_list = []
        num_of_items_sold = randint(1, 5)

        for x in range(1, num_of_items_sold + 1):
            product_variation = random.choice(self.product_variation_list)
            detail_dict = {
                'HEADER CODE': sale_invoice_header['CODE'],
                'PRODUCT VARIATION CODE': product_variation['CODE'],
                'QUANTITY': randint(5, 20)
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
            'CODE': f'OR-{len(self.official_receipt_header_list) + 1}',
            'DATE': self.current_date,
            'CREATOR': random.choice(self.sale_representative_list),
            'HEADER CODE': sale_invoice_header['CODE'],
            'STATUS': 'PAID',
        }

        return receipt_header_dict

    def create_official_receipt_detail(self, sale_invoice_header, official_receipt_header):
        detail_list = []

        for sale_invoice_detail in self.sale_invoice_detail_list:
            if sale_invoice_detail['HEADER CODE'] == sale_invoice_header['CODE']:
                # create random issue in quantity_paid to simulate real life
                quantity_paid = 0
                issue_is = randint(1, 10)
                if issue_is <= 1:  # 10% chance of issue
                    print('created issue in official receipt detail')
                    quantity_paid = randint(
                        sale_invoice_detail['QUANTITY'] - 3, sale_invoice_detail['QUANTITY'] + 20)
                else:
                    quantity_paid = sale_invoice_detail['QUANTITY']

                detail_dict = {
                    'HEADER CODE': official_receipt_header['CODE'],
                    'PRODUCT VARIATION CODE': sale_invoice_detail['PRODUCT VARIATION CODE'],
                    'QUANTITY': sale_invoice_detail['QUANTITY']
                }

                detail_list.append(detail_dict)

        return detail_list

    def create_official_receipt_transactions(self):
        #
        for sale_invoice_header in self.sale_invoice_header_list:
            if sale_invoice_header['STATUS'] == 'OPEN (FOR PAYMENT)':
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
                        if product_variation['CODE'] == official_receipt_detail['PRODUCT VARIATION CODE']:
                            product_variation['current_quantity'] = product_variation['current_quantity'] - \
                                official_receipt_detail['QUANTITY']

                #
                sale_invoice_header['STATUS'] = 'CLOSED'

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
            num_customer_today = randint(5, 20)
            for x in range(1, num_customer_today + 1):
                #
                self.create_sale_invoice_transactions()
                #
                self.create_official_receipt_transactions()

            #
            self.reset_product_variant_arriving_quantity()
            self.current_date += timedelta(days=1)

    def export_excel(self):
        output_dir = os.path.join(os.getcwd(), "dummy_transactions")
        os.makedirs(output_dir, exist_ok=True)

        # Mapping of lists to their corresponding filenames
        file_mapping = {
            "seed_purchases_purchaserequestheader.xlsx": self.purchase_request_header_list,
            "seed_purchases_purchaserequestdetail.xlsx": self.purchase_request_detail_list,
            "seed_purchases_purchasereceiveheader.xlsx": self.purchase_receive_header_list,
            "seed_purchases_purchasereceivedetail.xlsx": self.purchase_receive_detail_list,
            "seed_sales_saleinvoiceheader.xlsx": self.sale_invoice_header_list,
            "seed_sales_saleinvoicedetail.xlsx": self.sale_invoice_detail_list,
            "seed_sales_officialreceiptheader.xlsx": self.official_receipt_header_list,
            "seed_sales_officialreceiptdetail.xlsx": self.official_receipt_detail_list,
        }

        for filename, data_list in file_mapping.items():
            if data_list:  # Only create files for non-empty lists
                file_path = os.path.join(output_dir, filename)
                pd.DataFrame(data_list).to_excel(file_path, index=False)
                self.stdout.write(self.style.SUCCESS(f"Saved {filename}"))

        self.stdout.write(self.style.SUCCESS(
            f"All dummy transactions have been exported to {output_dir}"))
