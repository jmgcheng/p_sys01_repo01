# p_sys01_repo01

## milestone - nn - milestone check - 12022024

- [ / ] - adding employee/user 1 is to 1
- [ / ] - employee can login, update profile, change password
- [ / ] - crud employee
- [ / ] - employee bulk insert, update button and management controls
- [ / ] - employee list - datatables - view, filter, pagination
- [ / ] - all db working
- [ / ] - docker working
- [ / ] - requirements.txt
- [ / ] - db backup working
- [ / ] - cleanup - code

## milestone - nn - milestone check - 12112024

- [ / ] - crud product
- [ / ] - crud product variation
- [ / ] - bulk insert product and product variation
- [ / ] - product list - datatable
- [ / ] - product variation - datatable
- [ / ] - cleanup - code

## milestone - nn - milestone check - 01212025

- [ / ] - crud purchase request. Has simple approving flow PurchaseRequestApproveView. An admin or has a correct group can approve purchase request in detail page No separate list for needed to be approve for now to make it simple. Can be modified someday for specific flow.
- [ / ] - add vendors app. Admin usage for now. No public crud
- [ / ] - add customers app. Admin usage for now. No public crud
- [ / ] - crud purchase receive. No strict flow yet. No updating of status yet. No checking other apps details yet.
- [ / ] - crud inventory add
- [ / ] - crud inventory deduct
- [ / ] - add sales invoice. No strict flow yet. No updating of status yet. No checking other apps details yet. No checking if all items are paid yet.
- [ / ] - add sales official receipt. No strict flow yet. No updating of status yet. No checking other apps details yet. No checking if all items are paid yet. Will only be use for inventory deduct. Can create (payment receipt) someday to auto attach in this transaction

## Issues/Notes - 01 - 01212025

- all apps as of now (purchase request/received, vendors, customers, inventory add/deduct, sales invoices, sales official receipt) flow are still loose.
- no transaction really auto updates their status of apps in transaction.
- this gives us simplicity for now for:
  - fast portfolio video recording
  - flexible for future changes in flow

## Issues/Notes - 02 - 01212025

- status attached to the apps are still not final and will depend on the final system flow
- clean migrations and models(default value) someday
- still not decided on the final flow as it can have possible flow
- always refer to notes at 'hc system/notes.txt'. Also we should update that notes in this repo

## Upcoming Todos - 01 - 01212025

- plan/finalize - eye candies for 1st apps of portfolio
- fix - filtering/sorting - datatables all needed columns - on different apps
- add/attach - apps details to parent transaction - eg show attached official receipts transaction in sales invoice detail. This is for easy manual approval someday if we approve manually and eye candy
- finalize - transaction flows - Note/Save 'hc system\notes.txt'
- implement - inventory quantity
- finalize - ui improvements
- create - management commands for all apps - if all flow are final and stable

## milestone - nn - milestone check - 02032025

- [ / ] - finalize - eye candies for 1st apps of portfolio
- [ / ] - fix - filtering/sorting - datatables all needed columns - on different apps
- [ / ] - add/attach - apps details to parent transaction
- [ / ] - do - simple transaction flows - Note/Save 'hc system\notes.txt'
- [ / ] - implement - inventory quantity
- [ / ] - create - management commands for all apps
- [ / ] - create - management commands - generate dummy transactions
- [ / ] - add - product variation - quantity alert
- [ / ] - add - pdf button - generate pdf
- [ / ] - add - charts
- [ / ] - add - business table data

## Upcoming Todos - 01 - 02032025

- find/test/apply - appropriate fonts
- find/test/apply - different ui improvements
- update/finalize - generated pdf templates
- apply - permissions for main menu and class
- retest/fix - docker compose setup
- cleanup - code
- resetup/clean - migration folders

## milestone - nn - milestone check - 02112025

- [ / ] - update - theme
- [ / ] - update - chart list - add more card
- [ / ] - update - pdf templates
- [ / ] - update - datatables - default sort column
- [ / ] - add - management command - generate dummy employees
- [ / ] - code cleanup
- [ / ] - test run - docker compose
- [ / ] - update - requirements.txt
- [ / ] - update - collectstatic

## Upcoming Todos - 01 - 02112025

- finalize - video flow - portfolio
- record - video - portfolio
- edit - video - portfolio
- upload/check - video - portfolio
- update - issue notes
- update - 'hc system/notes.txt'
- apply - permissions for main menu and class
- resetup/clean - migration folders

## milestone - nn - milestone check - 02272025

- [ / ] - finalize - video flow - portfolio
- [ / ] - record - video - portfolio
- [ / ] - edit - video - portfolio
- [ / ] - upload/check - video - portfolio
- [ ] -
- [ / ] - apply - django rest framework
- [ / ] - success test on api list, create, detail, update for product, product variation, employee, purchase request, purchase receive, sales invoice, official receipt, inventory summary using postman
- [ / ] - browsable api login at domain.com/api-auth/login/
- [ / ] - login/logout browsable api

## postman notes - 02272025

```
POST
http://127.0.0.1:8000/api/login/
body > form-data
username ...
password ...

GET
http://127.0.0.1:8000/api/products/
Headers
	Authorization 	Token a74...

POST
http://127.0.0.1:8000/api/products/
Headers
	Authorization 	Token a74...
Body > raw > json
{
    "code": "P-000004",
    "name": "API PRODUCT 01"
}

GET
http://127.0.0.1:8000/api/products/4
Headers
	Authorization 	Token a74...

PUT
http://127.0.0.1:8000/api/products/4/
Headers
	Authorization 	Token a74...
body > raw > json
{
    "code": "P-000004",
    "name": "API PRODUCT 01"
}

GET
http://127.0.0.1:8000/api/products/variations
Headers
	Authorization 	Token a74...

POST
http://127.0.0.1:8000/api/products/variations/
Headers
	Authorization 	Token a74...
body > raw > json
{
    "code": "PV-API-002",
    "product": 1,
    "name": "API PRODUCT VARIATION 02",
    "unit": 11,
    "size": null
}

GET
http://127.0.0.1:8000/api/products/variations/103
Headers
	Authorization 	Token a74...

PUT
http://127.0.0.1:8000/api/products/variations/103/
Headers
	Authorization 	Token a74...
body > raw > json
{
    "code": "PV-API-002 UPDATED",
    "product": 2,
    "name": "API PRODUCT VARIATION 02 UPDATED",
    "unit": 11,
    "size": null
}

GET
http://127.0.0.1:8000/api/employees/
Headers
	Authorization 	Token a74...

POST
http://127.0.0.1:8000/api/employees/
Headers
	Authorization 	Token a74...
body > raw > json
{
    "company_id": "API-EMP-0001",
    "gender": "MALE",
    "status": 1,
    "position": 1,
    "position_level": 1,
    "position_specialties": [1, 3],
    "first_name": "Api First Name 01",
    "last_name": "Api Last Name 01",
    "email": "api-email01@domain.com"
}

GET
http://127.0.0.1:8000/api/employees/101
Headers
	Authorization 	Token a74...

PUT
http://127.0.0.1:8000/api/employees/102/
Headers
	Authorization 	Token a74...
body > raw > json
{
    "company_id": "API-EMP-0001",
    "gender": "MALE",
    "status": 1,
    "position": 1,
    "position_level": 1,
    "position_specialties": [1, 3],
    "first_name": "Api First Name 01",
    "last_name": "Api Last Name 01",
    "email": "api-email01@domain.com"
}

GET
http://127.0.0.1:8000/api/purchase-requests/
Headers
	Authorization 	Token a74...

POST
http://127.0.0.1:8000/api/purchase-requests/
Headers
	Authorization 	Token a74...
body > raw > json
{
    "code": "PR-API-002",
    "date": "2024-02-27",
    "requestor": 1,
    "status": 1,
    "detail": [
        {
            "product_variation": 11,
            "quantity_request": 3
        },
        {
            "product_variation": 13,
            "quantity_request": 5
        }
    ]
}

GET
http://127.0.0.1:8000/api/purchase-requests/303
Headers
	Authorization 	Token a74...

PUT
http://127.0.0.1:8000/api/purchase-requests/304/
Headers
	Authorization 	Token a74...
body > raw > json
{
    "code": "PR-API-002",
    "date": "2024-02-27",
    "requestor": 1,
    "status": 1,
    "detail": [
        {
            "product_variation": 5,
            "quantity_request": 6
        },
        {
            "product_variation": 6,
            "quantity_request": 5
        }
    ]
}


http://127.0.0.1:8000/api/purchase-receives/
http://127.0.0.1:8000/api/purchase-receives/306/
http://127.0.0.1:8000/api/sale-invoices/
GET /api/sale-invoices/ → Returns the first 10 records
GET /api/sale-invoices/?page=2 → Returns the next 10 records
GET /api/sale-invoices/?page_size=20 → Returns 20 records per page
GET /api/sale-invoices/?page_size=50&page=2 → Gets the second page with 50 records per page
http://127.0.0.1:8000/api/sale-invoices/4696/
http://127.0.0.1:8000/api/official-receipts/
http://127.0.0.1:8000/api/official-receipts/4696/
http://127.0.0.1:8000/api/inventory-summary/

```

## Upcoming Todos - 01 - 02272025

- update - issue notes
- update - 'hc system/notes.txt'
- apply - permissions for main menu and class
- resetup/clean - migration folders
