$(document).ready(function() {
    console.log('employee_list.js ready');

    let table = $('#employeeTable').DataTable({
        processing: true,
        serverSide: true,
        scrollX: true,
        ajax: {
            url: "/employees/ajx_employee_list/",
            type: 'GET',
            data: function(d) {
                d.position = getCheckedValues('chkPosition');
                d.specialty = getCheckedValues('chkSpecialty');
                d.gender = getCheckedValues('chkGender');
                d.employee_status = getCheckedValues('chkEmployeeStatus');
            }
        },
        columns: [
            { data: 'company_id' },
            { data: 'start_date' },
            { data: 'last_name' },
            { data: 'first_name' },
            { data: 'middle_name' },
            { data: 'position' },
            { data: 'specialties' },
            { data: 'level' },
            { data: 'gender' },
            { data: 'status' },
        ],
        layout: {
            // topStart: 'pageLength',
            // topEnd: 'search',
            // bottomStart: 'info',
            // bottomEnd: 'paging'

            top2Start: 'pageLength',
            topStart: 'info',
            // top2End: 'paging',
            topEnd: 'search',
            bottomStart: 'info',
            bottomEnd: 'paging',
            // bottom2Start: 'info',
            // bottom2End: 'paging'
        },
        order: [[0, 'asc']],
        pageLength: 25,
    });

    function getCheckedValues(name) {
        var values = [];
        $('input[name="' + name + '"]:checked').each(function() {
            let val = $(this).val();

            if (name === 'chkEmployeeStatus' && val === 'ACTIVE') {
                values.push('PROBATION', 'REGULAR');
            }
            else {
                values.push(val);
            }
            return [...new Set(values)];  // Remove duplicates
        });
        return values;
    }
});