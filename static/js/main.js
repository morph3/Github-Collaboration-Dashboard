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