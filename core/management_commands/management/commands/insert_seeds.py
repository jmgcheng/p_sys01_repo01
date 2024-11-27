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


                # ('insert_new_departments_departmentcategory',
                #  'new_departments_departmentcategory.xlsx'),

                # ('insert_new_currencies_currency',
                #  'new_currencies_currency.xlsx'),

                # ('insert_new_countries_country', 'new_countries_country.xlsx'),
                # ('insert_new_countries_stateprovince',
                #  'new_countries_stateprovince.xlsx'),
                # ('insert_new_countries_citymunicipality',
                #  'new_countries_citymunicipality.xlsx'),

                # ('insert_new_offices_office', 'new_offices_office.xlsx'),
                # ('insert_new_offices_officeroom', 'new_offices_officeroom.xlsx'),

                # ('insert_new_business_codes_businesscodebrand',
                #  'new_business_codes_businesscodebrand.xlsx'),

                # ('insert_new_business_codes_businesscodeunit',
                #  'new_business_codes_businesscodeunit.xlsx'),
                # ('insert_new_business_codes_businesscode',
                #  'new_business_codes_businesscode.xlsx'),

                # ('insert_new_employees_employeejoblevel',
                #  'new_employees_employeejoblevel.xlsx'),
                # ('insert_new_employees_employeenationality',
                #  'new_employees_employeenationality.xlsx'),
                # ('insert_new_employees_employeeposition',
                #  'new_employees_employeeposition.xlsx'),
                # ('insert_new_employees_employeeseparationtype',
                #  'new_employees_employeeseparationtype.xlsx'),
                # ('insert_new_employees_employeestatus',
                #  'new_employees_employeestatus.xlsx')

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
