from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Run a series of management commands to insert new records.'

    def handle(self, *args, **kwargs):
        try:
            # List of commands to run with their respective arguments
            commands_to_run = [
                #
                ('seed_employees_employeestatus',
                 'seed_employees_employeestatus.xlsx'),
                #
                ('seed_employees_employeejoblevel',
                 'seed_employees_employeejoblevel.xlsx'),
                #
                ('seed_employees_employeejob',
                 'seed_employees_employeejob.xlsx'),
                #
                ('seed_employees_employeejobspecialty',
                 'seed_employees_employeejobspecialty.xlsx'),
                #
                ('seed_employees_employee',
                 'seed_employees_employee.xlsx'),

                #
                ('seed_products_productcolor',
                 'seed_products_productcolor.xlsx'),
                #
                ('seed_products_productsize',
                 'seed_products_productsize.xlsx'),
                #
                ('seed_products_productunit',
                 'seed_products_productunit.xlsx'),
                #
                ('seed_products_product',
                 'seed_products_product.xlsx'),
                #
                ('seed_products_productvariation',
                 'seed_products_productvariation.xlsx'),

                # Add more commands as needed
            ]

            for command_name, filename in commands_to_run:
                self.stdout.write(self.style.NOTICE(
                    f"Running {command_name} with {filename}..."))
                call_command(command_name, filename)
                self.stdout.write(self.style.SUCCESS(
                    f"Successfully ran {command_name}"))

        except CommandError as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))

        self.stdout.write(self.style.SUCCESS(
            'All commands have been successfully executed.'))
