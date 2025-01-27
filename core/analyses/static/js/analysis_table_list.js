$(document).ready(function() {
    console.log('analysis_table_list.js ready');

    let tbl_EDA = $('#tableEmployeeDemographicsAge').DataTable({
        processing: true,
        ajax: {
            url: "/analyses/ajx_employee_demographics_age/",
            dataSrc: "data",
        },
        columns: [
            { data: "age", title: "Age" },
            { data: "male", title: "Male" },
            { data: "female", title: "Female" },
            { data: "total", title: "Grand Total" }
        ],
        scrollX: true,
        bFilter: false,
        responsive: true,
        autoWidth: false,
    });


    let tbl_TP = $('#tableTopProducts').DataTable({
        processing: true,
        ajax: {
            url: "/analyses/ajx_top_products/",
            dataSrc: "data",
        },
        columns: [
            { data: 'product_variation'},
            { data: 'product'},
            { data: 'purchase_requested'},
            { data: 'purchase_received'},
            { data: 'sale_invoice'},
            { data: 'official_receipt'},
        ],
        scrollX: true,
        bFilter: false,
        responsive: true,
        autoWidth: false,
    });


    let tbl_SBC = $('#tableSalesBreakdownCategory').DataTable({
        processing: true,
        ajax: {
            url: "/analyses/ajx_sales_breakdown_category/",
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


    // let tbl_TSV = $('#tableTopSellingVariations').DataTable({
    //     processing: true,
    //     ajax: {
    //         url: "/analyses/ajx_top_selling_variations/",
    //         dataSrc: "data",
    //     },
    //     columns: [
    //         { "data": "col_1" },
    //         { "data": "col_2" },
    //     ],
    //     scrollX: true,
    //     bFilter: false,
    //     responsive: true,
    //     autoWidth: false,
    // });


    // let tbl_MSVP = $('#tableMonthlySalesVsPurchases').DataTable({
    //     processing: true,
    //     ajax: {
    //         url: "/analyses/ajx_monthly_sales_vs_purchases/",
    //         dataSrc: "data",
    //     },
    //     columns: [
    //         { "data": "col_1" },
    //         { "data": "col_2" },
    //     ],
    //     scrollX: true,
    //     bFilter: false,
    //     responsive: true,
    //     autoWidth: false,
    // });


    // let tbl_RPS = $('#tableReceiptsPaymentStatus').DataTable({
    //     processing: true,
    //     ajax: {
    //         url: "/analyses/ajx_receipts_payment_status/",
    //         dataSrc: "data",
    //     },
    //     columns: [
    //         { "data": "col_1" },
    //         { "data": "col_2" },
    //     ],
    //     scrollX: true,
    //     bFilter: false,
    //     responsive: true,
    //     autoWidth: false,
    // });


    // let tbl_PP = $('#tablePatientPurchases').DataTable({
    //     processing: true,
    //     ajax: {
    //         url: "/analyses/ajx_patient_purchases/",
    //         dataSrc: "data",
    //     },
    //     columns: [
    //         { "data": "col_1" },
    //         { "data": "col_2" },
    //     ],
    //     scrollX: true,
    //     bFilter: false,
    //     responsive: true,
    //     autoWidth: false,
    // });

    
    //readjust column width to make sure their 100%
    $('#collapseEDA, #collapseTP, #collapseSBC').on('shown.bs.collapse', function () {
        tbl_EDA.columns.adjust().draw();
        tbl_TP.columns.adjust().draw();
        tbl_SBC.columns.adjust().draw();
        // tbl_TSV.columns.adjust().draw();
        // tbl_MSVP.columns.adjust().draw();
        // tbl_RPS.columns.adjust().draw();
        // tbl_PP.columns.adjust().draw();
    });

});