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

        let str = "Commit based truck factor, calculates target system by processing its evolution history. Algorithm determines how many commits each user has on all files, and it assigns a Degree of Author value to each user for each file. From these values, it declares users who are above the threshold as the author of the file. If a user has enough authored files, it puts that user in the truck factor list.";
        str += "<br>";
        str += "This truck factor is calculated based on the AVL algorithm from A Novel Approach for Estimating Truck Factors paper which was written by Guilherme Avelino, Leonardo Passos, Andre Hora, and Marco Tulio Valente.";
        str += "<br>"
        elem.innerHTML = str;

    } else if (idx == 1) {
        let str = "Heuristic based truck factor, is composed of 6 steps, respectively File analysis, Developer Knowledge calculation, Key developers identification, Tuner, Truck factor assessment. The algorithm detects how much knowledge each user has about each file. If the user's knowledge of the file is above the primary threshold, the user is considered the primary developer of that file, or if it is above the secondary rather than the primary threshold, the user is considered the secondary developer. If it is not secondary, it is assumed that the user does not know anything about that file. Depending on the developer type, the algorithm gives different values to different users and puts users whose total knowledge value is above the threshold into the truck factor list";
        str += "<br>"
        str += "This truck factor is calculated based on the CST Algorithm from Assessing the bus factor of Git repositories paper which was written by Valerio Cosentino, Javier Cánovas Izquierdo, Jordi Cabot.";
        str += "<br>"
        elem.innerHTML = str;

    } else if (idx == 2) {
      let str = "Stack based truck factor, determines how many commits each user has on all files, and it assigns a Degree of Author value to each user for each file. If a user has enough degree of author value, it puts that user in the truck factor list.";
      str += "<br>"
      str += "This truck factor is calculated based on modified version of the commit based truck factor.";
      str += "<br>"
      elem.innerHTML = str;

    }



}
