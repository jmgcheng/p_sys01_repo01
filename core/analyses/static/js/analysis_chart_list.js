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


    const ctx2 = document.getElementById('topProductVariation').getContext('2d');
    fetch("/analyses/ajx_chart_top_products/")
        .then(response => response.json())
        .then(data => {
            new Chart(ctx2, {
                type: "line",
                data: {
                    labels: data.labels,
                    datasets: data.datasets,
                },
                options: {
                    responsive: true,
                    scales: {
                        xAxes: [
                            {
                                scaleLabel: {
                                    display: true,
                                    labelString: "Months",
                                },
                            },
                        ],
                        yAxes: [
                            {
                                scaleLabel: {
                                    display: true,
                                    labelString: "Quantity",
                                },
                            },
                        ],
                    },
                    title: {
                        display: true,
                        text: "Top Product Variation - Monthly Trends",
                    },
                },
            });
        })
        .catch(error => console.error("Error fetching top product data:", error));

    const ctx3 = document.getElementById('salesBreakdownCategory').getContext('2d');
    fetch("/analyses/ajx_chart_sales_breakdown_category/")
        .then((response) => response.json())
        .then((data) => {
            new Chart(ctx3, {
                type: "pie",
                data: {
                    labels: data.labels,
                    datasets: data.datasets,
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "top",
                        },
                        tooltip: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    const dataset = tooltipItem.dataset;
                                    const value = dataset.data[tooltipItem.dataIndex];
                                    const total = dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(2);
                                    return `${tooltipItem.label}: ${value} (${percentage}%)`;
                                },
                            },
                        },
                    },
                },
            });
        })
        .catch((error) => console.error("Error fetching sales breakdown data:", error));


    $('.pdf-chart').click(function (e) {
        e.preventDefault();
        const targetChart = $(this).attr('chart');
        const targetTitle = $(this).attr('title');
        const targetBlurb = $(this).attr('blurb');
    
        try {
            const canvas = document.getElementById(targetChart);
            const imgData = canvas.toDataURL("image/png", 1.0); // High-quality image
    
            const pdf = new jsPDF({ unit: "mm", format: [279, 216] }); // Short bond paper (8.5" x 11")
    
            // Page size
            const pageWidth = 216;  
            const pageHeight = 279; 
    
            // Title & Paragraph
            const title = targetTitle; // Dynamic Title
            const paragraph = targetBlurb; 
    
            // Title Position
            const marginLeft = 15;  // Left margin
            let currentY = 20;      // Start Y position
    
            pdf.setFontSize(18);
            pdf.text(title, marginLeft, currentY); // Title at (x=15, y=20)
    
            // Paragraph Position
            pdf.setFontSize(12);
            const splitText = pdf.splitTextToSize(paragraph, pageWidth - 30); // Wrap text properly
            currentY += 10; // Move down after title
            pdf.text(splitText, marginLeft, currentY); 
    
            // Calculate height of paragraph
            const paragraphHeight = splitText.length * 6; // Approximate line height
            currentY += paragraphHeight + 10; // Move below paragraph with spacing
    
            // Scale and Position Chart (70% of page width)
            const scaleFactor = 0.7; // Adjusted to 70%
            const imgScaledWidth = pageWidth * scaleFactor;
            const imgScaledHeight = (imgScaledWidth / canvas.width) * canvas.height; // Maintain aspect ratio
    
            // Center Chart
            const xOffset = (pageWidth - imgScaledWidth) / 2;
    
            // Place Chart below paragraph
            pdf.addImage(imgData, "PNG", xOffset, currentY, imgScaledWidth, imgScaledHeight);
    
            // save automatically
            // pdf.save(targetTitle + ".pdf");

             // Open PDF in new tab instead of downloading
            const pdfBlob = pdf.output("blob"); // Convert PDF to Blob
            const pdfUrl = URL.createObjectURL(pdfBlob); // Create Blob URL
            window.open(pdfUrl, "_blank"); // Open in new tab
        } 
        catch (error) {
            console.error("Error generating PDF:", error);
        }
    });
        
        
        
});