var table_nutrient;

function nutrient_dt(food_c, search_str_nutrient = "") {

    // Get a list of currently visible columns
    let cols = [];
    if ($("#nutrient_table_wrapper").find("th").length > 0) {
        $.each($("#nutrient_table_wrapper").find("th"), function (i, k) {
            cols.push(k.innerText);
        });
        // Get the unique values
        cols = cols.filter((item, i, ar) => ar.indexOf(item) === i);
    } else {
        cols = ["Nutrient", "Nutrient symbol", "Value", "Unit", "Standard Error", "number of observations", "source c", "ref c",
            "date entry", "usda source", "usda derivation", "tagname", "publication code"]
    }

    cols = cols.map(function (i) {
        return i.toLowerCase()
    });


    s = '/api/nutrient/?food_c=' + food_c + "&format=datatables";
    table_nutrient = $('#nutrient_table').DataTable({
        // "serverSide": true, // Breaks searching
        "processing": true,
        "destroy": true,
        "scrollX": true,
        "scrollY": true,
        "dom": 'BZfrtip', // Adds button and resize
        "select": true,
        "pageLength": 200,
        "ajax": s,
        "colReorder": true,
        "bFilter": false,
        "altEditor": true,
        "searching": true,
        "oSearch": {"sSearch": search_str_nutrient},
        "columns": [
            {"data": "NUTR.SEQUENCE_C", "visible": false, "className": "noVis"},
            {"data": "NUTR_AMOUNT_C", "visible": false, "className": "noVis"},
            {"data": "FOOD", "visible": false, "className": "noVis"},
            {"data": "NUTR.NUTR_NAME", visible: cols.includes("nutrient"), "title": "Nutrient"}, // These 4 are defined by the serializer
            {"data": "NUTR.NUTR_SYMBOL", visible: cols.includes("nutrient symbol"), "title": "Nutrient symbol"},
            {"data": "NUTR_VALUE", visible: cols.includes("value"), "title": "Value"},
            {"data": "NUTR.UNIT", visible: cols.includes("unit"), "title": "Unit"},
            {"data": "STD_ERROR", visible: cols.includes("standard error"), 'title': "Standard Error"},
            {"data": "NUM_OBSER", visible: cols.includes("number of observations"), 'title': "Number of observations"},
            {"data": "NUTR_C", visible: cols.includes("source c"), "title": "Source c"},
            {"data": "REF_C", visible: cols.includes("ref c"), "title": "Ref c"},
            {"data": "DATE_ENTRY", visible: cols.includes("date entry"), "title": "Date entry"},
            {"data": "USDA_SOURCE", visible: cols.includes("usda source"), "title": "USDA source"},
            {"data": "USDA_DERIV", visible: cols.includes("usda derivation"), "title": "USDA derivation"},
            {"data": "NUTR.TAGNAME", visible: cols.includes("tagname"), "title": "Tagname"},
            {"data": "PUBLICATION_CODE", visible: cols.includes("publication code"), "title": "Publication Code"},

        ],
        buttons: [
            {
                extend: 'colvis',
                // columns: ':not(.noVis)'
                columns: ':gt(1)' // Skip the first n-1 columns
            },
            {
                text: 'Edit',
                name: 'edit'
            },
            {
                text: 'History',
                name: 'history',
                action: function (e, dt, node, config) {
                    var adata = dt.rows({
                        selected: true
                    });
                    let nutr_c = adata.data()[0]["NUTR_AMOUNT_C"];
                    window.location.href = "/history/nutrient_history/" + nutr_c;
                }
            },
            {
                text: 'Reset',
                name: 'reset',
                action: function (e, dt, node, config) {
                    table_nutrient.order([[0, "asc"]]).draw();
                }
            }],
        onEditRow: function (datatable, rowdata, success, error) {

            s = '/api/nutrient_update/' + rowdata['NUTR_AMOUNT_C'] + "/";

            $.ajaxSetup({
                headers: {"X-CSRFToken": csrftoken}
            });

            // Remove things that should not be changed
            delete rowdata["NUTR.SEQUENCE_C"];
            delete rowdata["NUTR_AMOUNT_C"];
            delete rowdata["NUTR_C"];
            delete rowdata["REF_C"];
            delete rowdata["FOOD_C"];

            delete rowdata["DATE_ENTRY"];


            $.ajax({
                url: s,
                type: 'PUT',
                data: rowdata,
                success: success,
                error: error
                //error: function (jqXHR, textStatus, errorThrown) {
                //    console.log(jqXHR.responseText);
                //},
            });

            // Make it so the modal can scroll again
            $("#nutrient_modal").css('overflow-y', 'auto');
        }
    });


    // table = $('#foodandgroup_table').DataTable();
    $('#search_box').keyup(function () {
        table_nutrient.draw();
    });

    //$('#search_box').on('keypress', function(e) {
     //   table_nutrient.draw();
    //});

    // See http://live.datatables.net/nayerize/1/edit
    //table_nutrient.columns().every(function() {
    //    var index = this.index();
    //    var header = $('#nutrient_table thead th[data-column-index=' + index + ']')
    //     header.addClass('sorting');
    //     header.removeClass('sorting_disabled');
    // });


}


$.fn.dataTable.ext.search.push(
    function (settings, data, dataIndex) {
        if ($("#search_box").val() == "") {
            return true
        }
        searches = $("#search_box").val().split(" OR ");
        for (i = 0; i < searches.length; i++) {
            s = searches[i].toUpperCase();
            if (data[3].includes(s)) {
                return true;
            }
        }
        return false;
    }
);
