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
- finalize - ui improvements
- create - management commands for all apps - if all flow are final and stable
