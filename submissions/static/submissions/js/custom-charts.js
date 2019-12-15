$(document).ready(function () {

        let $excelPagination = $('#excel-pagination');
        let $excelTable = $('#excel-table');
        let pageNumber = 1;
        let $body = $('body');
        let start = moment().startOf('year');
        let end = moment();
        let showAllColumns = 0;
        let progressFilter = [];
        let classificationFilter = [];
        let liabilityFilter = [];
        let supplierFilter = [];
        let lastUpdated = null; // variable to track when the charts were last updated

        let startDate = start.format("YYYY-MM-DD");
        let endDate = end.format("YYYY-MM-DD");

        let charts = [];
        let adminCharts = null;

        $.ajax({
            url: '/api/charts',
            method: 'GET'
        }).done(response => {
            adminCharts = response;
        }).fail(error => {
            console.log(error);
        });

        updateTimeFilter(start, end); // update time filter for the first time;

        function updateTimeFilter(start, end) {
            $("#fr-date-range .date-range p").html(
                'Period Filter: &nbsp;' + '<strong>' + start.format("YYYY-MM-DD") + " - " + end.format("YYYY-MM-DD") + '</strong>'
            );
            startDate = start.format("YYYY-MM-DD");
            endDate = end.format("YYYY-MM-DD");
            handleFiltersChange(true, true, true, true);
        }

        $("#fr-date-range .date-range").daterangepicker(
            {
                startDate: start,
                endDate: end,
                opens: 'left',
                ranges: {
                    Today: [moment(), moment()],
                    Yesterday: [
                        moment().subtract(1, "days"),
                        moment().subtract(1, "days")
                    ],
                    "Current Week": [moment().subtract(1, "weeks"), moment()],
                    "Previous Week": [
                        moment()
                            .subtract(1, "week")
                            .startOf("week"),
                        moment()
                            .subtract(1, "week")
                            .endOf("week")
                    ],
                    "Current Month": [moment().startOf("month"), moment().endOf("month")],
                    "Previous Month": [
                        moment()
                            .subtract(1, "month")
                            .startOf("month"),
                        moment()
                            .subtract(1, "month")
                            .endOf("month")
                    ],
                    "Current Quarter": [moment().startOf("Q"), moment().endOf("Q")],
                    "Previous Quarter": [
                        moment()
                            .subtract(1, "Q")
                            .startOf("Q"),
                        moment()
                            .subtract(1, "Q")
                            .endOf("Q")
                    ],
                    "Current Year": [moment().startOf("year"), moment().endOf("year")],
                    "Previous Year": [
                        moment()
                            .subtract(1, "year")
                            .startOf("year"),
                        moment()
                            .subtract(1, "year")
                            .endOf("year")
                    ]
                }
            },
            updateTimeFilter
        );

        $body.delegate('#show-all-columns', 'click', function () {
            showAllColumns = $('#show-all-columns').prop('checked') ? 1 : 0;
            loadTableData();
        });

        $body.delegate('#excel-download-button', 'click', function () {

            let url = '/excel_download?' + $.param({
                showAllColumns: showAllColumns
            });

            window.open(url);
        });

        $body.on('change', '#supplier-select', function (e) {
            handleFiltersChange(true, false, false, false);
        });

        $body.on('change', '#liability-select', function (e) {
            handleFiltersChange(false, true, false, false);
        });

        $body.on('change', '#progress-select', function (e) {
            handleFiltersChange(false, false, true, false);
        });

        $body.on('change', '#classification-select', function (e) {
            handleFiltersChange(false, false, false, true);
        });

        $body.delegate('.page-item', 'click', function (e) {
            e.preventDefault();
            pageNumber = $(this).attr('data-page-number');
            loadTableData();
        });

        function handleFiltersChange(supplierChanged = false, liabilityChanged = false, progressChanged = false, classificationChanged = false) {
            let tempSupplierFilter = [];
            let tempLiabilityFilter = [];
            let tempProgressFilter = [];
            let tempClassificationFilter = [];

            if (supplierChanged) {
                $('#supplier-select option:selected').each(function (i) {
                    tempSupplierFilter.push($(this).val())
                });
                supplierFilter = tempSupplierFilter;
            }

            if (liabilityChanged) {
                $('#liability-select option:selected').each(function (i) {
                    tempLiabilityFilter.push($(this).val())
                });
                liabilityFilter = tempLiabilityFilter;
            }

            if (progressChanged) {
                $('#progress-select option:selected').each(function (i) {
                    tempProgressFilter.push($(this).val());
                });
                progressFilter = tempProgressFilter;
            }

            if (classificationChanged) {
                $('#classification-select option:selected').each(function (i) {
                    tempClassificationFilter.push($(this).val());
                });
                classificationFilter = tempClassificationFilter;
            }

            let filterData = {
                progressFilter: progressFilter,
                supplierFilter: supplierFilter,
                liabilityFilter: liabilityFilter,
                classificationFilter: classificationFilter
            };

            $.ajax({
                url: '/api/update_submission_ids/' + startDate + '/' + endDate,
                data: filterData,
                method: 'GET'
            }).done(response => {
                drawCharts();
            }).fail(error => {
                console.log(error);
            })
        }

        function drawRadarChart(canvasId, labels, data, step, maxValue) {

            let radarChart = new Chart(canvasId, {
                type: "radar",
                data: {
                    labels: labels,
                    datasets: data.map(
                        entry => {
                            return {
                                label: entry.label,
                                backgroundColor: entry.background_color,
                                borderColor: "#4c84ff",
                                pointBorderWidth: 2,
                                pointRadius: 4,
                                pointBorderColor: "rgba(76,132,255,1)",
                                pointBackgroundColor: "#ffffff",
                                data: entry.data
                            }
                        }
                    )
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: false
                    },
                    title: {
                        display: false,
                        text: "Chart.js Radar Chart"
                    },
                    layout: {
                        padding: {
                            top: 10,
                            bottom: 10,
                            right: 10,
                            left: 10
                        }
                    },
                    scale: {
                        ticks: {
                            beginAtZero: true,
                            fontColor: "#1b223c",
                            fontSize: 12,
                            stepSize: step,
                            max: maxValue
                        }
                    },
                    tooltips: {
                        titleFontColor: "#888",
                        bodyFontColor: "#555",
                        titleFontSize: 12,
                        bodyFontSize: 14,
                        backgroundColor: "rgba(256,256,256,0.95)",
                        displayColors: true,
                        borderColor: "rgba(220, 220, 220, 0.9)",
                        borderWidth: 2
                    }
                }
            });

            charts.push(radarChart);
        }

        function drawDoughNutChart(canvasId, labels, data, backgroundColors) {


            let myDoughnutChart = new Chart(canvasId, {
                type: "doughnut",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: labels,
                            data: data,
                            backgroundColor: backgroundColors,
                            borderWidth: 1
                            // borderColor: ['#4c84ff','#29cc97','#8061ef','#fec402']
                            // hoverBorderColor: ['#4c84ff', '#29cc97', '#8061ef', '#fec402']
                        }
                    ]

                },
                cutoutPercentage: 75,
                tooltips: {
                    callbacks: {
                        title: function (tooltipItem, data) {
                            return "Order : " + data["labels"][tooltipItem[0]["index"]];
                        },
                        label: function (tooltipItem, data) {
                            return data["datasets"][0]["data"][tooltipItem["index"]];
                        }
                    },
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 14,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    displayColors: true,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2
                }

            });

            charts.push(myDoughnutChart);
        }

        function drawPolarChart(canvasId, labels, data, backgroundColors, step, maxValue) {

            let configPolar = {
                type: 'polarArea',
                data: {
                    datasets: [
                        {
                            data: data,
                            backgroundColor: backgroundColors,
                            label: "" // for legend
                        }
                    ],
                    labels: labels
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        position: "right",
                        display: false
                    },
                    layout: {
                        padding: {
                            top: 10,
                            bottom: 10,
                            right: 10,
                            left: 10
                        }
                    },
                    title: {
                        display: false,
                        text: "Chart.js Polar Area Chart"
                    },
                    scale: {
                        ticks: {
                            beginAtZero: true,
                            fontColor: "#1b223c",
                            fontSize: 12,
                            stepSize: step,
                            max: maxValue
                        },
                        reverse: false
                    },
                    animation: {
                        animateRotate: false,
                        animateScale: true
                    },
                    tooltips: {
                        titleFontColor: "#888",
                        bodyFontColor: "#555",
                        titleFontSize: 12,
                        bodyFontSize: 14,
                        backgroundColor: "rgba(256,256,256,0.95)",
                        displayColors: true,
                        borderColor: "rgba(220, 220, 220, 0.9)",
                        borderWidth: 2
                    }
                },
                title: {
                    display: false,
                    text: "Chart.js Polar Area Chart"
                },
                scale: {
                    ticks: {
                        beginAtZero: true,
                        fontColor: "#1b223c",
                        fontSize: 12,
                        stepSize: step,
                        max: maxValue
                    },
                    reverse: false
                },
                animation: {
                    animateRotate: false,
                    animateScale: true
                },
                tooltips: {
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 14,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    displayColors: true,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2
                }

            };

            let polarChart = new Chart(canvasId, configPolar);
            charts.push(polarChart);
        }


        function drawMultipleStats(canvasId, labels, data, stepSize) {

            var msdChart = new Chart(canvasId, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: data.map((entry) => {
                        return {
                            label: entry.label,
                            pointRadius: 4,
                            pointBackgroundColor: "rgba(255,255,255,1)",
                            pointBorderWidth: 2,
                            fill: true,
                            lineTension: 0,
                            backgroundColor: entry.background_color,
                            borderWidth: 2.5,
                            borderColor: entry.border_color,
                            data: entry.data
                        }
                    })
                },
                options: {
                    maintainAspectRatio: false,
                    legend: {
                        display: false
                    },
                    scales: {
                        xAxes: [
                            {
                                gridLines: {
                                    drawBorder: true,
                                    display: false
                                },
                                ticks: {
                                    display: true, // hide main x-axis line
                                    beginAtZero: true,
                                    fontFamily: "Roboto, sans-serif",
                                    fontColor: "#8a909d"
                                }
                            }
                        ],
                        yAxes: [
                            {
                                gridLines: {
                                    drawBorder: true, // hide main y-axis line
                                    display: true
                                },
                                ticks: {
                                    callback: function (value) {
                                        var ranges = [
                                            {divider: 1e6, suffix: "M"},
                                            {divider: 1e3, suffix: "k"}
                                        ];

                                        function formatNumber(n) {
                                            for (var i = 0; i < ranges.length; i++) {
                                                if (n >= ranges[i].divider) {
                                                    return (
                                                        (n / ranges[i].divider).toString() + ranges[i].suffix
                                                    );
                                                }
                                            }
                                            return n;
                                        }

                                        return formatNumber(value);
                                    },
                                    stepSize: stepSize,
                                    fontColor: "#8a909d",
                                    fontFamily: "Roboto, sans-serif",
                                    beginAtZero: true
                                }
                            }
                        ]
                    },
                    tooltips: {
                        enabled: true
                    }
                }
            });

            charts.push(msdChart);
        }


        function drawProductLineCharts(canvasId, labels, data) {

            var config = {
                // The type of chart we want to create
                type: "line",
                // The data for our dataset
                data: {
                    labels: labels,
                    datasets: data.map((entry) => {
                        return {
                            label: entry.label,
                            backgroundColor: "transparent",
                            borderColor: entry.border_color,
                            data: entry.data,
                            lineTension: 0,
                            pointRadius: 5,
                            pointBackgroundColor: "rgba(255,255,255,1)",
                            pointHoverBackgroundColor: "rgba(255,255,255,1)",
                            pointBorderWidth: 2,
                            pointHoverRadius: 7,
                            pointHoverBorderWidth: 1
                        }
                    })
                },
                // Configuration options go here
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: false
                    },
                    scales: {
                        xAxes: [
                            {
                                gridLines: {
                                    display: false,
                                },
                                ticks: {
                                    fontColor: "#8a909d", // this here
                                },
                            }
                        ],
                        yAxes: [
                            {
                                gridLines: {
                                    fontColor: "#8a909d",
                                    fontFamily: "Roboto, sans-serif",
                                    display: true,
                                    color: "#eee",
                                    zeroLineColor: "#eee"
                                },
                                ticks: {
                                    // callback: function(tick, index, array) {
                                    //   return (index % 2) ? "" : tick;
                                    // }
                                    stepSize: 50,
                                    fontColor: "#8a909d",
                                    fontFamily: "Roboto, sans-serif"
                                }
                            }
                        ]
                    },
                    tooltips: {
                        mode: "index",
                        intersect: false,
                        titleFontColor: "#888",
                        bodyFontColor: "#555",
                        titleFontSize: 12,
                        bodyFontSize: 15,
                        backgroundColor: "rgba(256,256,256,0.95)",
                        displayColors: true,
                        xPadding: 10,
                        yPadding: 7,
                        borderColor: "rgba(220, 220, 220, 0.9)",
                        borderWidth: 2,
                        caretSize: 6,
                        caretPadding: 5
                    }
                }
            };

            let chart = new Chart(canvasId, config);
            charts.push(chart);
        }

        function drawMultiBarCharts(canvasId, labels, data, maxHeight) {

            let chart = new Chart(canvasId, {
                // The type of chart we want to create
                type: "bar",

                // The data for our dataset
                data: {
                    labels: labels,
                    datasets: data.map(entry => {
                        return {
                            label: entry.label,
                            backgroundColor: entry.background_color,
                            borderColor: entry.border_color,
                            data: entry.data,
                            pointBackgroundColor: "rgba(76, 132, 255,0)",
                            pointHoverBackgroundColor: "rgba(76, 132, 255,1)",
                            pointHoverRadius: 3,
                            pointHitRadius: 30
                        }
                    })

                },

                // Configuration options go here
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: false
                    },
                    scales: {
                        xAxes: [
                            {
                                gridLines: {
                                    display: false
                                }
                            }
                        ],
                        yAxes: [
                            {
                                gridLines: {
                                    display: true
                                },
                                ticks: {
                                    beginAtZero: true,
                                    stepSize: maxHeight / 10,
                                    fontColor: "#8a909d",
                                    fontFamily: "Roboto, sans-serif",
                                    max: maxHeight
                                }
                            }
                        ]
                    },
                    tooltips: {}
                }
            });

            charts.push(chart);
        }

        function drawLineChart(canvasId, labels, data) {

            let chart = new Chart(canvasId, {
                // The type of chart we want to create
                type: "line",

                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "",
                            backgroundColor: "transparent",
                            borderColor: "rgb(82, 136, 255)",
                            data: data,
                            lineTension: 0.3,
                            pointRadius: 5,
                            pointBackgroundColor: "rgba(255,255,255,1)",
                            pointHoverBackgroundColor: "rgba(255,255,255,1)",
                            pointBorderWidth: 2,
                            pointHoverRadius: 8,
                            pointHoverBorderWidth: 1
                        }
                    ]
                },

                // Configuration options go here
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: false
                    },
                    layout: {
                        padding: {
                            right: 10
                        }
                    },
                    scales: {
                        xAxes: [
                            {
                                gridLines: {
                                    display: false
                                }
                            }
                        ],
                        yAxes: [
                            {
                                gridLines: {
                                    display: true,
                                    color: "#eee",
                                    zeroLineColor: "#eee",
                                },
                                ticks: {
                                    callback: function (value) {
                                        var ranges = [
                                            {divider: 1e6, suffix: "M"},
                                            {divider: 1e4, suffix: "k"}
                                        ];

                                        function formatNumber(n) {
                                            for (var i = 0; i < ranges.length; i++) {
                                                if (n >= ranges[i].divider) {
                                                    return (
                                                        (n / ranges[i].divider).toString() + ranges[i].suffix
                                                    );
                                                }
                                            }
                                            return n;
                                        }

                                        return formatNumber(value);
                                    }
                                }
                            }
                        ]
                    },
                    tooltips: {
                        callbacks: {
                            title: function (tooltipItem, data) {
                                return data["labels"][tooltipItem[0]["index"]];
                            },
                            label: function (tooltipItem, data) {
                                return "$" + data["datasets"][0]["data"][tooltipItem["index"]];
                            }
                        },
                        responsive: true,
                        intersect: false,
                        enabled: true,
                        titleFontColor: "#888",
                        bodyFontColor: "#555",
                        titleFontSize: 12,
                        bodyFontSize: 18,
                        backgroundColor: "rgba(256,256,256,0.95)",
                        xPadding: 20,
                        yPadding: 10,
                        displayColors: false,
                        borderColor: "rgba(220, 220, 220, 0.9)",
                        borderWidth: 2,
                        caretSize: 10,
                        caretPadding: 15
                    }
                }
            });

            charts.push(chart);
        }

        function drawBarChart(canvasId, labels, data, chartLabel) {
            let barChart = new Chart(canvasId, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: chartLabel,
                            data: data,
                            backgroundColor: "#4c84ff"
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: false
                    },
                    scales: {
                        xAxes: [
                            {
                                gridLines: {
                                    drawBorder: false,
                                    display: false
                                },
                                ticks: {
                                    display: true,
                                    beginAtZero: true,
                                    autoSkip: false
                                }
                            }
                        ],
                        yAxes: [
                            {
                                gridLines: {
                                    drawBorder: true,
                                    display: false
                                },
                                ticks: {
                                    display: false,
                                    beginAtZero: true
                                }
                            }
                        ]
                    },
                    tooltips: {
                        titleFontColor: "#888",
                        bodyFontColor: "#555",
                        titleFontSize: 12,
                        bodyFontSize: 15,
                        backgroundColor: "rgba(256,256,256,0.95)",
                        displayColors: false,
                        borderColor: "rgba(220, 220, 220, 0.9)",
                        borderWidth: 2
                    }
                }
            });
            charts.push(barChart);
        }


        function drawDualLineChart(canvasId, labels, data) {

            console.log(labels);
            let chart = new Chart(canvasId, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: data.map((entry) => {
                        return {
                            label: entry.label,
                            pointRadius: 4,
                            pointBackgroundColor: "rgba(255,255,255,1)",
                            pointBorderWidth: 2,
                            fill: false,
                            backgroundColor: "transparent",
                            borderWidth: 2,
                            borderColor: entry.border_color,
                            data: entry.data
                        }
                    })
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: {
                        padding: {
                            right: 10
                        }
                    },

                    legend: {
                        display: true
                    },
                    scales: {
                        xAxes: [
                            {
                                gridLines: {
                                    display: false,
                                },
                                ticks: {
                                    fontColor: "#8a909d", // this here
                                },
                            }
                        ],
                        yAxes: [
                            {
                                gridLines: {
                                    drawBorder: false, // hide main y-axis line
                                    display: false
                                },
                                ticks: {
                                    display: false,
                                    beginAtZero: true
                                }
                            }
                        ]
                    },
                    tooltips: {
                        titleFontColor: "#888",
                        bodyFontColor: "#555",
                        titleFontSize: 12,
                        bodyFontSize: 14,
                        backgroundColor: "rgba(256,256,256,0.95)",
                        displayColors: true,
                        borderColor: "rgba(220, 220, 220, 0.9)",
                        borderWidth: 2
                    }
                }
            });

            charts.push(chart);
        }

        function drawPieChart(canvasId, labels, data, backgroundColors) {
            let pieChart = new Chart(canvasId, {
                type: "pie",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "Who is at Fault",
                            data: data,
                            backgroundColor: backgroundColors,
                            borderWidth: 1
                        }
                    ]

                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: true
                    },
                    tooltips: {
                        titleFontColor: "#888",
                        bodyFontColor: "#555",
                        titleFontSize: 12,
                        bodyFontSize: 14,
                        backgroundColor: "rgba(256,256,256,0.95)",
                        drabackgroundColor: "rgba(256,256,256,0.95)",
                        displayColors: true,
                        borderColor: "rgba(220, 220, 220, 0.9)",
                        borderWidth: 2
                    }
                }
            });
            charts.push(pieChart);
        }

        function drawChart(chartData) {

            // Destroy existing charts

            let chartSelect = $('#' + chartData.slug);
            let endPoint = chartData.end_point;


            $.ajax({
                url: endPoint,
                method: 'GET'
            }).done(response => {

                switch (chartData.chart_type) {
                    case 'pie_chart':
                        response.data && response.labels && drawPieChart(chartSelect, response.labels, response.data, response.background_colors);
                        break;

                    case 'constant_value':
                        chartSelect.text(response.metric);
                        break;


                    case 'polar_chart':
                        response.data && response.labels && drawPolarChart(chartSelect, response.labels, response.data, response.background_colors, response.step, response.max_value);
                        break;

                    case 'bar_chart':
                        response.data && response.labels && drawBarChart(chartSelect, response.labels, response.data);
                        break;

                    case 'donut_chart':
                        response.data && response.labels && drawDoughNutChart(chartSelect, response.labels, response.data, response.background_colors);
                        break;

                    case 'radar_chart':
                        response.labels && response.data && drawRadarChart(chartSelect, response.labels, response.data, response.step, response.max_value);
                        break;

                    case 'multiple_statistics':
                        response.labels && response.datasets && drawMultipleStats(chartSelect, response.labels, response.datasets, response.step_size);
                        break;

                    case 'product_line':
                        response.labels && response.datasets && drawProductLineCharts(chartSelect, response.labels, response.datasets);
                        break;

                    case 'multiple_bar_chart':
                        response.labels && response.datasets && drawMultiBarCharts(chartSelect, response.labels, response.datasets, response.max_height);
                        break;


                    case 'dual_line_chart':
                        response.labels && response.datasets && drawDualLineChart(chartSelect, response.labels, response.datasets);
                        break;

                    case 'line_chart':
                        response.labels && response.data && drawLineChart(chartSelect, response.labels, response.data);
                        break;

                    default:
                        console.log(response)
                }

            }).fail(error => {
                console.log(error);
            });
        }


        function drawCharts() {

            if (adminCharts) {
                while (charts.length > 0) {
                    let chart = charts.pop();
                    chart.destroy();
                }
                adminCharts.map(chartData => {
                    drawChart(chartData);
                });

                loadTableData();
            }
        }

        function loadTableData() {

            let url = '/excel_table';

            let requestData = {
                pageNumber: pageNumber,
                showAllColumns: showAllColumns
            };

            $.ajax({
                url: url,
                data: requestData,
                success: function (response) {
                    $excelTable.html(response.excel_table);
                    $excelPagination.html(response.pagination);
                    $excelTable.stickyTable({overflowy: true});
                },
                error: function (err) {
                    console.log(err);
                }
            });
        }
    }
);

