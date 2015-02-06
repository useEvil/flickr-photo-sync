function handleFiles(files) {
    $.fn.editable.defaults.mode = 'inline';
    $.fn.editable.defaults.onblur = 'submit';
    $.fn.editable.defaults.showbuttons = false;
    // Check for the various File API support.
    if (window.FileReader) {
        // FileReader are supported.
        getAsText(files[0]);
    } else {
        alert('FileReader are not supported in this browser.');
    }
}

function getAsText(fileToRead) {
    var reader = new FileReader();
    // Handle errors load
    reader.onload = loadHandler;
    reader.onerror = errorHandler;
    // Read file into memory as UTF-8
    reader.readAsText(fileToRead);
}

function loadHandler(event) {
    var csv_string = event.target.result;
    processData(csv_string);
}

function processData(csv_string) {
    var lines = CSV.parse(csv_string)
    drawOutput(lines);
}

function errorHandler(evt) {
    if (evt.target.error.name == "NotReadableError") {
        alert("Canno't read file !");
    }
}

function drawOutput(lines) {
    //Clear previous data
    document.getElementById("csv_output").innerHTML = "";
    var table = document.createElement("table");
    table.className = 'csv_output';
    for (var i = 0; i < lines.length; i++) {
        var row = table.insertRow(-1);
        if (i === 0) {
            row.className = 'csv_output row_header';
        } else {
            row.className = 'csv_output edit_row';
        }

        // row numbers
        var numberCell = row.insertCell(-1);
        numberCell.className = 'csv_output';
        numberCell.appendChild(document.createTextNode(i));

        for (var j = 0; j < lines[i].length; j++) {
            var firstNameCell = row.insertCell(-1);
            if (i === 0) {
                firstNameCell.className = 'csv_output cell_header';
            } else {
                firstNameCell.className = 'csv_output edit_cell';
            }
            firstNameCell.id = i+'_'+j;
            firstNameCell.setAttribute('data-type', 'text');
            firstNameCell.appendChild(document.createTextNode(lines[i][j]));
        }
    }
    document.getElementById("csv_output").appendChild(table);
    $('.edit_cell').editable();
}

function submitTableRows() {
    // row headers
    var headers = { };
    $('.cell_header').each(function (i, cell) {
        var $cell = $(cell);
        headers[i] = $cell.text();
    });

    // row cells
    $('.edit_row').each(function (i, row) {
        var $row = $(row);
        var $cells = $row.find('.edit_cell');
        var data = { };

        $cells.map(function (i, cell) {
            var $cell = $(cell);
            data[headers[i]] = $cell.text();
        });

        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: JSON.stringify(data),
            dataType: 'json'
        }).fail(function (data) {
            console.log("Response Error: " + JSON.stringify(data));
        }).done(function (data) {
            console.log("Response Done: " + JSON.stringify(data));
        }).always(function (data) {
            console.log("Response Always: " + JSON.stringify(data));
        });
    });
}