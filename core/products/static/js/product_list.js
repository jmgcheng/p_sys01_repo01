$(document).ready(function() {
    console.log('product_list.js ready');

    let table = $('#dataTable').DataTable({
        processing: true,
        serverSide: true,
        scrollX: true,
        ajax: {
            url: "/products/ajx_product_list/",
            type: 'GET',
            data: function(d) {}
        },
        columns: [
            { data: 'code' },
            { data: 'name' },
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