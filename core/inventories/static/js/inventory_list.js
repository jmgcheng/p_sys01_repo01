$(document).ready(function() {
    console.log('inventory_list.js ready');

    let table = $('#dataTable').DataTable({
        processing: true,
        serverSide: true,
        scrollX: true,
        ajax: {
            url: "/inventories/ajx_inventory_list/",
            type: 'GET',
            data: function(d) {}
        },
        columns: [
            { data: 'code' },
            { data: 'name' },
            { data: 'product' },
            { data: 'qty_manual_add' },
            { data: 'qty_manual_deduct' },
            { data: 'qty_purchasing' },
            { data: 'qty_purchasing_receive' },
            { data: 'qty_sale_releasing' },
            { data: 'qty_sold' },
            { data: 'qty_on_hand' },
        ],
        layout: {
            // topStart: 'pageLength',
            // topEnd: 'search',
            // bottomStart: 'info',
            // bottomEnd: 'paging'

            // top2Start: 'pageLength',
            topStart: 'search',
            top2End: 'info',
            topEnd: 'pageLength',

            bottomStart: 'paging',
            bottomEnd: 'info',
            // bottom2Start: 'info',
            // bottom2End: 'paging'
        },
        order: [[0, 'asc']],
        pageLength: 25,
    });

    
});