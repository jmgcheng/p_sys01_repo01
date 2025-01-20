$(document).ready(function() {
    console.log('inventory_add_list.js ready');

    let table = $('#dataTable').DataTable({
        processing: true,
        serverSide: true,
        scrollX: true,
        ajax: {
            url: "/inventories/adds/ajx_inventory_add_list/",
            type: 'GET',
            data: function(d) {}
        },
        columns: [
            { data: 'code' },
            { data: 'date' },
            { data: 'adder' },
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
        order: [[0, 'desc']],
        pageLength: 50,
    });
    
});