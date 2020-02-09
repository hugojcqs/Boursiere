var db = {};
var current_quarter = 0;



function _disable_past_history() {
    //get_current_quarter();
    $('.history_btn').each(function() {
        let btn = $(this);
        if (parseInt(btn.data("id")) != current_quarter) {
            btn.attr('onclick', '');
            btn.removeClass("history_btn");
            btn.addClass("disabled");
        }
    });
    get_next_update_and_disable_past_history();
}

function set_clickable_order_button() {
    if (_can_order()) {
        $('#order_btn').removeClass("disabled")
    } else {
        $('#order_btn').addClass("disabled")
    }
}


function plus(i, beer_name) {
    let input = $("#input" + beer_name);
    let new_v_input = Number(input.val()) + 1;
    input.val(new_v_input);
    db[beer_name] = new_v_input;
    console.log(JSON.stringify(db));
}

function minus(i, beer_name) {
    let input = $("#input" + beer_name);
    let new_v_input = Number(input.val()) - 1;

    if (new_v_input >= 0) {
        input.val(new_v_input);
        db[beer_name] = new_v_input;
        console.log(JSON.stringify(db));
    }
}

function calculate_price() {

}

function check_order_stock(data) {

}

function make_order() {

}

function _add_history(json_) {
    time = json_['time'];
    token = json_['token'];
    text = json_['text'];
    total_price = json_['total_price'];
    raw_html = `<a class="list-group-item list-group-item-action flex-column align-items-start text-white " style="background-color:#8b9dc3;" id="${token}"><div class="d-flex w-100 justify-content-between"><h5 class="mb-1">Commande n°${token}</h5><small>${time}</small><div class="btn btn-sm btn-danger history_btn" data-id="${current_quarter}" onclick="delete_histo(${token}, ${current_quarter})">Supprimer</div></div><p class="mb-1">${text}</p><small>Prix total : ${total_price} €</small></a>`;
    $('#histo').prepend(raw_html)
}

function delete_histo(token, quarter) {

}

function hide_bar(bar) {
    $(".bar" + bar.toString()).hide();
}

function show_bar(bar) {
    $(".bar" + bar.toString()).show();
}
