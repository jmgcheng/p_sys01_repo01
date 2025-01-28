$(document).ready(function() {
    console.log('analysis_chart_list.js ready');

    const ctx1 = document.getElementById('employeeDemographicsAge').getContext('2d');

    fetch("/analyses/ajx_chart_employee_demographics_age/")
        .then(response => response.json())
        .then(data => {
            new Chart(ctx1, {
                type: "pie",
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: "Employee Age Distribution",
                            data: data.data,
                            backgroundColor: [
                                "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#E7E9ED"
                            ],
                            hoverBackgroundColor: [
                                "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#E7E9ED"
                            ],
                        },
                    ],
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: "Employee Age Distribution",
                    },
                },
            });
        })
        .catch(error => console.error("Error fetching age demographics data:", error));

});