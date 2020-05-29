// var table_nutrient;
// var editor;
// var z;
// var cell;
//
// editor = new $.fn.dataTable.Editor({
//     table: "#nutrient_table",
//     idSrc: "NUTR_AMOUNT_C",
//     // Important for making it submit the change on tab
//     formOptions: {
//         inline: {
//             onBlur: 'submit'
//         }
//     },
//     ajax: function (method, url, data, success, error) {
//
//         let nutrient_amount_c = Object.keys(data.data)[0];
//         s = '/api/nutrient_update/' + nutrient_amount_c + "/";
//
//         $.ajaxSetup({
//             headers: {"X-CSRFToken": csrftoken}
//         });
//
//         $.ajax({
//             url: s,
//             data: JSON.stringify(data.data[nutrient_amount_c]),
//             dataType: "json",
//             type: "PUT",
//             success: function (json) {
//                 success(json);
//             },
//             error: function (xhr, error2, thrown) {
//                 error(xhr, error2, thrown);
//             }
//         });
//     },
//
//     fields: [
//         {label: "SEQUENCE_C", name: "NUTR.NUTR_AMOUNT_C"},
//         {label: "NUTR_AMOUNT_C", name: "NUTR_AMOUNT_C"},
//         {label: "FOOD", name: "FOOD"},
//         {label: "Nutrient", name: "NUTR.NUTR_NAME"},
//         {label: "Nutrient symbol", name: "NUTR.NUTR_SYMBOL"},
//         {label: "Value", name: "NUTR_VALUE"},
//         {label: "Unit", name: "NUTR.UNIT"},
//         {label: "STD_ERROR", name: "STD_ERROR"},
//         {label: "NUM_OBSER", name: "NUM_OBSER"},
//
//         {label: "NUTR_C", name: "NUTR_C"},
//         {label: "REF_C", name: "REF_C"},
//         {label: "DATE_ENTRY", name: "DATE_ENTRY"},
//         {label: "USDA_SOURCE", name: "USDA_SOURCE"},
//         {label: "USDA_DERIV", name: "USDA_DERIV"},
//         {label: "NUTR_TAGNAME", name: "NUTR.TAGNAME"},
//         {label: "PUBLICATION_CODE", name: "PUBLICATION_CODE"},
//
//     ]
// });
//
//
// function nutrient_dt(food_c, search_str_nutrient = "") {
//
//     // Get a list of currently visible columns
//     let cols = [];
//     if ($("#nutrient_table_wrapper").find("th").length > 0) {
//         $.each($("#nutrient_table_wrapper").find("th"), function (i, k) {
//             cols.push(k.innerText);
//         });
//         // Get the unique values
//         cols = cols.filter((item, i, ar) => ar.indexOf(item) === i);
//     } else {
//         cols = ["Nutrient", "Nutrient symbol", "Value", "Unit", "Standard Error", "number of observations", "source c", "ref c",
//             "date entry", "usda source", "usda derivation", "tagname", "publication code"]
//     }
//
//     cols = cols.map(function (i) {
//         return i.toLowerCase()
//     });
//
//
//     s = '/api/nutrient/?food_c=' + food_c + "&format=datatables";
//     table_nutrient = $('#nutrient_table').DataTable({
//         // "serverSide": true, // Breaks searching
//         "processing": true,
//         "destroy": true,
//         "scrollX": true,
//         "scrollY": true,
//         //"dom": 'BZfrtip', // Adds button and resize
//         "dom": 'Bfrtip',
//         keys: {
//             columns: ':not(:first-child)',
//             keys: [9],
//             editor: editor,
//             editOnFocus: true
//         },
//         select: {
//             style: 'os',
//             selector: 'td:first-child'
//         },
//         "pageLength": 200,
//         "ajax": s,
//         "colReorder": true,
//         "bFilter": false,
//         "searching": true,
//         "oSearch": {"sSearch": search_str_nutrient},
//         "columns": [
//             {"data": "NUTR.SEQUENCE_C", "visible": false, "className": "noVis"},
//             {"data": "NUTR_AMOUNT_C", "visible": false, "className": "noVis"},
//             {"data": "FOOD", "visible": false, "className": "noVis"},
//             {"data": "NUTR.NUTR_NAME", visible: cols.includes("nutrient"), "title": "Nutrient"}, // These 4 are defined by the serializer
//             {"data": "NUTR.NUTR_SYMBOL", visible: cols.includes("nutrient symbol"), "title": "Nutrient symbol"},
//             {"data": "NUTR_VALUE", visible: cols.includes("value"), "title": "Value"},
//             {"data": "NUTR.UNIT", visible: cols.includes("unit"), "title": "Unit"},
//             {"data": "STD_ERROR", visible: cols.includes("standard error"), 'title': "Standard Error"},
//             {"data": "NUM_OBSER", visible: cols.includes("number of observations"), 'title': "Number of observations"},
//             {"data": "NUTR_C", visible: cols.includes("source c"), "title": "Source c"},
//             {"data": "REF_C", visible: cols.includes("ref c"), "title": "Ref c"},
//             {"data": "DATE_ENTRY", visible: cols.includes("date entry"), "title": "Date entry"},
//             {"data": "USDA_SOURCE", visible: cols.includes("usda source"), "title": "USDA source"},
//             {"data": "USDA_DERIV", visible: cols.includes("usda derivation"), "title": "USDA derivation"},
//             {"data": "NUTR.TAGNAME", visible: cols.includes("tagname"), "title": "Tagname"},
//             {"data": "PUBLICATION_CODE", visible: cols.includes("publication code"), "title": "Publication Code"},
//         ],
//         buttons: [
//             {
//                 text: 'Edit mode',
//                 name: 'edit',
//                 attr: {
//                     id: 'edit_button'
//                 },
//
//                 action: function (e, dt, node, config) {
//                     if (!$("#edit_button").hasClass("pushed")) {
//                         $("#edit_button").addClass("pushed");
//                         table_nutrient.keys.enable();
//                     } else {
//                         $("#edit_button").removeClass("pushed");
//                         // Next two lines deselect the current selected cell
//                         editor.close();
//                         $(".focus").removeClass("focus");
//                         table_nutrient.keys.disable();
//                     }
//                 }
//             },
//
//             {
//                 text: 'History',
//                 name: 'history',
//                 action: function (e, dt, node, config) {
//                     var adata = dt.rows({
//                         selected: true
//                     });
//                     let nutr_c = adata.data()[0]["NUTR_AMOUNT_C"];
//                     window.location.href = "/history/nutrient_history/" + nutr_c;
//                 }
//             },
//         ]
//     });
//
//
//     $('#search_box').keyup(function () {
//         table_nutrient.draw();
//     });
//
// }

//
// $.fn.dataTable.ext.search.push(
//     function (settings, data, dataIndex) {
//         console.log("test123");
//         console.log(data);
//         if ($("#search_box").val() == "") {
//             return true
//         }
//         searches = $("#search_box").val().split(" OR ");
//         for (i = 0; i < searches.length; i++) {
//             s = searches[i].toUpperCase();
//             if (data[3].includes(s)) {
//                 return true;
//             }
//         }
//         return false;
//     }
// );
