$(document).ready(function() {
    console.log('product_variation_list.js ready');

    let table = $('#dataTable').DataTable({
        processing: true,
        serverSide: true,
        scrollX: true,
        ajax: {
            url: "/products/variations/ajx_product_variation_list/",
            type: 'GET',
            data: function(d) {
                d.product = getCheckedValues('chkProduct');
                d.unit = getCheckedValues('chkUnit');
                d.size = getCheckedValues('chkSize');
                d.color = getCheckedValues('chkColor');
            }
        },
        columns: [
            { data: 'code' },
            { data: 'name' },
            { data: 'size' },
            { data: 'unit' },
            { data: 'color' },
            { data: 'product' },
            { data: 'quantity_alert' },
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

    $('input[type=checkbox][name=chkProduct], input[type=checkbox][name=chkUnit], input[type=checkbox][name=chkSize], input[type=checkbox][name=chkColor]').change(function() {
        let groupName = $(this).attr("name");
        // get the master checkbox for this group
        let groupAllCheckbox = $('#'+groupName+'-0');
        // 
        // get the other group checkbox that is not master 
        let otherCheckboxes = $('input[type=checkbox][name='+groupName+']').not(groupAllCheckbox);
        
        // is this the master your changing?
        if ($(this).is(groupAllCheckbox)) {
            if (groupAllCheckbox.prop('checked')) {
                otherCheckboxes.prop('checked', true);
            } else {
                otherCheckboxes.prop('checked', false);
            }
        } else {
            if (otherCheckboxes.filter(':checked').length === otherCheckboxes.length) {
                groupAllCheckbox.prop('checked', true);
            } else {
                groupAllCheckbox.prop('checked', false);
            }
        }
        table.draw();
    });

    $('#resetFilters').on('click', function() {
        $('form select').each(function(index) {
            $(this).val('');
        })
        $('#dataTable_filter input').val('');
        $("input[type=radio][value='']").prop('checked', true);
        $("input[type=checkbox][customType='datatableFilter']").prop('checked', false);
        $('.collapse').collapse('hide');
        table.page.len(25).draw();
        table.order([0, 'asc']).draw();
        table.search('').draw();
        table.columns().search('');
        table.draw();
    });

    function getCheckedValues(name) {
        var values = [];
        $('input[name="' + name + '"]:checked').each(function() {
            let val = $(this).val();
            values.push(val);

            return [...new Set(values)];  // Remove duplicates
        });
        return values;
    }

    
});