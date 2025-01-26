$(document).ready(function() {
    console.log('analysis_table_list.js ready');

    let tbl_ED = $('#tableEmployeeDemographics').DataTable({
        processing: true,
        ajax: {
            url: "/analyses/ajx_employee_demographics/",
            dataSrc: "data",
        },
        columns: [
            { "data": "col_1" },
            { "data": "col_2" },
        ],
        scrollX: true,
        bFilter: false,
        responsive: true,
        autoWidth: false,
    });


    let tbl_TRI = $('#tableTopRequestedItems').DataTable({
        processing: true,
        ajax: {
            url: "/analyses/ajx_top_requested_items/",
            dataSrc: "data",
        },
        columns: [
            { "data": "col_1" },
            { "data": "col_2" },
        ],
        scrollX: true,
        bFilter: false,
        responsive: true,
        autoWidth: false,
    });


    let tbl_SB = $('#tableSalesBreakdown').DataTable({
        processing: true,
        ajax: {
            url: "/analyses/ajx_sales_breakdown/",
            dataSrc: "data",
        },
        columns: [
            { "data": "col_1" },
            { "data": "col_2" },
        ],
        scrollX: true,
        bFilter: false,
        responsive: true,
        autoWidth: false,
    });


    let tbl_TSV = $('#tableTopSellingVariations').DataTable({
        processing: true,
        ajax: {
            url: "/analyses/ajx_top_selling_variations/",
            dataSrc: "data",
        },
        columns: [
            { "data": "col_1" },
            { "data": "col_2" },
        ],
        scrollX: true,
        bFilter: false,
        responsive: true,
        autoWidth: false,
    });


    let tbl_MSVP = $('#tableMonthlySalesVsPurchases').DataTable({
        processing: true,
        ajax: {
            url: "/analyses/ajx_monthly_sales_vs_purchases/",
            dataSrc: "data",
        },
        columns: [
            { "data": "col_1" },
            { "data": "col_2" },
        ],
        scrollX: true,
        bFilter: false,
        responsive: true,
        autoWidth: false,
    });


    let tbl_RPS = $('#tableReceiptsPaymentStatus').DataTable({
        processing: true,
        ajax: {
            url: "/analyses/ajx_receipts_payment_status/",
            dataSrc: "data",
        },
        columns: [
            { "data": "col_1" },
            { "data": "col_2" },
        ],
        scrollX: true,
        bFilter: false,
        responsive: true,
        autoWidth: false,
    });


    let tbl_PP = $('#tablePatientPurchases').DataTable({
        processing: true,
        ajax: {
            url: "/analyses/ajx_patient_purchases/",
            dataSrc: "data",
        },
        columns: [
            { "data": "col_1" },
            { "data": "col_2" },
        ],
        scrollX: true,
        bFilter: false,
        responsive: true,
        autoWidth: false,
    });

    
    //readjust column width to make sure their 100%
    $('#collapseED, #collapseTRI, #collapseSB, #collapseTSV, #collapseMSVP, #collapseRPS, #collapsePP').on('shown.bs.collapse', function () {
        tbl_ED.columns.adjust().draw();
        tbl_TRI.columns.adjust().draw();
        tbl_SB.columns.adjust().draw();
        tbl_TSV.columns.adjust().draw();
        tbl_MSVP.columns.adjust().draw();
        tbl_RPS.columns.adjust().draw();
        tbl_PP.columns.adjust().draw();
    });

});