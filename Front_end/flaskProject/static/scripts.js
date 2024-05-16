$(document).ready(function() {
    // Static data for dropdowns
    var airlines = ["SpiceJet", "AirAsia", "Vistara", "GO FIRST", "Indigo", "Air India", "Trujet"];
    var cities = ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"];
    var flight_classes = ["Business", "Economy"];
    var no_of_stops = Array.from({length: 10}, (_, i) => i.toString()); // Creates an array from 0 to 9
    var times = [
        {'label': 'Evening', 'value': 'Evening'},
        {'label': 'Early Morning', 'value': 'Early Morning'},
        {'label': 'Morning', 'value': 'Morning'},
        {'label': 'Afternoon', 'value': 'Afternoon'},
        {'label': 'Night', 'value': 'Night'}
    ];

    // Function to populate dropdowns
    function populateDropdown(selector, options, isObject = false) {
        var dropdown = $(selector);
        dropdown.empty(); // Clear existing options
        $.each(options, function(index, item) {
            if (isObject) {
                dropdown.append($('<option></option>').attr('value', item.value).text(item.label));
            } else {
                dropdown.append($('<option></option>').attr('value', item).text(item));
            }
        });
    }
    let predictionChart; // Keep the chart instance globally

    // Assuming this function is triggered and the 'results' array is available
    function plotPredictions(results) {
        const ctx = document.getElementById('prediction-chart').getContext('2d');
        const labels = results.map(data => data.days_left);
        const data = results.map(data => data.predicted_price);

        // Calculate minimum and maximum values for y-axis
        const minValue = Math.min(...data);
        const maxValue = Math.max(...data);
        const yAxisMin = minValue - ((maxValue - minValue) * 0.1); // reduce by 10% of the range

        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(75, 192, 192, 1)');
        gradient.addColorStop(1, 'rgba(75, 192, 192, 0)');

        if (predictionChart) { // If a chart instance exists, destroy it
            predictionChart.destroy();
        }

        predictionChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Predicted Airfare Change for Selected Date',
                    data: data,
                    fill: true,
                    backgroundColor: gradient,
                    borderColor: 'rgb(75, 192, 192)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: 'rgb(255, 99, 132)',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointStyle: 'rectRounded',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                tooltips: {
                    enabled: true,
                    mode: 'index',
                    intersect: false,
                    bodyFontSize: 14,
                    titleFontSize: 14,
                    backgroundColor: 'rgba(0,0,0,0.7)',
                    bodyFontColor: '#fff',
                    titleFontColor: '#fff',
                    callbacks: {
                        label: function(tooltipItem, data) {
                            return `Price: $${tooltipItem.yLabel.toFixed(2)}`;
                        }
                    }
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        fontColor: 'rgb(75, 192, 192)',
                        fontSize: 14
                    }
                },
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Price ($)',
                            fontSize: 16
                        },
                        gridLines: {
                            display: true,
                            color: "rgba(75, 192, 192, 0.2)"
                        },
                        ticks: {
                            beginAtZero: false,
                            suggestedMin: yAxisMin, // Start y-axis slightly below the minimum data value
                            fontSize: 12
                        }
                    }],
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Days Left',
                            fontSize: 16
                        },
                        gridLines: {
                            display: false
                        },
                        ticks: {
                            fontSize: 12
                        }
                    }]
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutBack'
                }
            }
        });
    }

    // Populate dropdowns on load
    populateDropdown('#airline', airlines);
    populateDropdown('#source-city', cities);
    populateDropdown('#dest-city', cities);
    populateDropdown('#flight-class', flight_classes);
    populateDropdown('#num-stops', no_of_stops);
    populateDropdown('#dep-time-category', times, true);
    populateDropdown('#arr-time-category', times, true);

    // modifcations
    // Set the minimum date for the date picker to today
    $('#travel-date').attr('min', new Date().toISOString().split('T')[0]);

    // Calculate days left when a new date is picked
    // $('#travel-date').on('change', function() {
    //
    // });


    //
    // // Update displayed range values
    // $('#days-left-slider').on('input', function() {
    //     $('#days-left-value').text($(this).val() + ' days');
    // });

    $('#flight-duration-slider').on('input', function() {
        $('#flight-duration-value').text($(this).val() + ' hours');
    });

    $('#predictionForm').on('submit', function(e) {
        e.preventDefault();

        var travelDate = $('#travel-date').val(); // Get the value of the date input
    if (!travelDate) {
        alert('Please select a travel date.');
        return; // Stop the form submission
    }

    var travelDateObj = new Date(travelDate);
    var currentDate = new Date();
    var timeDiff = travelDateObj - currentDate;
    var daysLeft = Math.ceil(timeDiff / (1000 * 3600 * 24));

    if (isNaN(daysLeft)) {
        alert('Invalid date selected.');
        return; // Stop the form submission
    }

    var formData = $(this).serialize() + '&days_left=' + daysLeft;
    $('#airplane-icon').css({'display': 'block', 'transform': 'translate(-50%, -50%)'}); // Show and position the airplane

        $.ajax({
            url: '/predict',
            type: 'POST',
            data: formData,
            success: function(result) {
                console.log('Received data:', result);
                //$('#prediction-output').html(result);
                plotPredictions(result);
                setTimeout(() => {
                $('#airplane-icon').css({
                    'display': 'none',
                    'transform': 'none'
                });
            }, 3000);
            },
            error: function() {
                $('#prediction-output').html('Error in prediction. Please check inputs.');
                $('#airplan e-icon').css('display', 'none'); // Hide icon on error
            }
        });
    });
});