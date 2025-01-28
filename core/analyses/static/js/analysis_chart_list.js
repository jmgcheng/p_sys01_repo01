$(document).ready(function() {
    console.log('analysis_chart_list.js ready');

    const ctx1 = document.getElementById('employeeDemographicsAge').getContext('2d');
    fetch("/analyses/ajx_chart_employee_demographics_age/")
        .then(response => response.json())
        .then(data => {
            new Chart(ctx1, {
                type: "bar",
                data: {
                    labels: data.labels,
                    datasets: data.datasets,
                },
                options: {
                    responsive: true,
                    scales: {
                        xAxes: [
                            {
                                stacked: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: "Age Groups",
                                },
                            },
                        ],
                        yAxes: [
                            {
                                stacked: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: "Number of Employees",
                                },
                            },
                        ],
                    },
                    title: {
                        display: true,
                        text: "Employee Demographics by Age and Gender",
                    },
                },
            });
        })
        .catch(error => console.error("Error fetching age demographics data:", error));

});