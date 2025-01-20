$(document).ready(function() {
    console.log('purchase_receive_list.js ready');

    let table = $('#dataTable').DataTable({
        processing: true,
        serverSide: true,
        scrollX: true,
        ajax: {
            url: "/purchases/receives/ajx_purchase_receive_list/",
            type: 'GET',
            data: function(d) {}
        },
        columns: [
            { data: 'code' },
            { data: 'request_code' },
            { data: 'date' },
            { data: 'receiver' },
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