function disable_refresh() {
    if (event.preventDefault) {
        event.preventDefault();
    } else {
        event.returnValue = false;
    }
}

function open_user_search_modal() {

    $("#searchInputLabel").html("Username:");
    $("#searchModalLabel").html("Enter Username");
    $('#searchFormId').attr('action', '/user?u=');
    $('#searchInputId').attr('placeholder', 'Enter username, for ex: "SerenityOS"');

    $('#searchModal').modal('toggle');

}

function open_repo_search_modal() {
    $("#searchInputLabel").html("Repository Name:");
    $("#searchModalLabel").html("Enter Repository Name");
    $('#searchFormId').attr('action', '/repository?r=');

    $('#searchInputId').attr('placeholder', 'Enter full repository name, for ex: "SerenityOS/serenity"');

    $('#searchModal').modal('toggle');
}


function do_search() {
    var search_type = $('#searchFormId').attr('action');
    var search_term = $('#searchInputId').val();
    var search_url = search_type + search_term;
    //console.log(`Location is ${search_url}`);
    //alert(search_url);
    window.location.href = search_url;
}

function update_truck_factor_info(idx) {
    console.log(`Updating truck factor selector to ${idx}`);

    let elem = document.querySelector("#currentVariantParagraphId");

    if (idx == 0) {

        let str = "Commit based truck factor,";
        str += "<br>";
        str += "This truck factor is calculated based on ...";
        str += "<br>"
        elem.innerHTML = str;

    } else if (idx == 1) {
        let str = "Heuristic based truck factor,";
        str += "<br>"
        str += "This truck factor is calculated based on ...";
        str += "<br>"
        elem.innerHTML = str;

    } else if (idx == 2) {
        elem.innerHTML = "Blame based truck factor";

    }



}