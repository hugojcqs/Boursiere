var db = {};
var current_quarter = 0;
var first_run = true;
$(document).ready(function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    get_next_update_and_disable_past_history();
});



function _can_order() {
    for (let key in db) {
        if (db.hasOwnProperty(key)) {
            if (db[key] > 0) return true;
        }
    }
}


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


function get_next_update_and_disable_past_history() {
    $.post({
        url: '/timer_to_next_up/',
        data: {
            'data': 'none'
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            let time_to_update = data.time_remaining;
            current_quarter = data.quarter;
            if (first_run) {
                _disable_past_history();
                first_run = false;
            }
            if (time_to_update > 0) {
                setTimeout(_disable_past_history, time_to_update * 1000 - 1000);
            } else {
                setTimeout(get_next_update_and_disable_past_history, 20 * 1000);
            }
        },
        error: function(xhr, status, error) {
            //TODO : handle error in ajax request
            console.log('Cannot update the stock page', status, error);
        }
    });
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
    set_clickable_order_button();
    calculate_price();
}

function minus(i, beer_name) {
    let input = $("#input" + beer_name);
    let new_v_input = Number(input.val()) - 1;

    if (new_v_input >= 0) {
        input.val(new_v_input);
        db[beer_name] = new_v_input;
        set_clickable_order_button();
        calculate_price();
    }

}

function calculate_price() {
    $.post({
        url: '/calculate_price/',
        data: {
            'data': JSON.stringify(db)
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            let elem = $("#total_price");
            elem.text('Prix : ' + String(data['price']) + " €");
            check_order_stock(data['now_stock']);

        },
        error: function(xhr, status, error) {
            //TODO : handle error in ajax request
            console.log('Cannot update the stock page', status, error);
        }
    });
}

function check_order_stock(data){
  // get all conserned beer
  data = JSON.parse(data)
  for(var beer_name in data){

    let input = $("#input" + beer_name);   //get input of beer card
    if(input.val() >= data[beer_name]){   //if input upper or equal than beer stock block plus button
      $('#plus'+beer_name).css("pointer-events", "none"); // disable + button
      $('#card_title_'+beer_name).css("text-decoration", "line-through");
    } else {
        $('#plus'+beer_name).css("pointer-events", "auto"); // enable + button
        $('#card_title_'+beer_name).css("text-decoration", "none");
    }


  }

}

function make_order() {
    if (!_can_order())
        return;

    $.post({
        url: '/make_order/',
        data: {
            'data': JSON.stringify(db)
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            _add_history(data);
            $(".input-number").val(0);
            $("#total_price").text('Prix : 0 €');
            db = {}
        },
        error: function(xhr, status, error) {
            //TODO : handle error in ajax request
            console.log('Cannot update the stock page', status, error);
        }
    });
}

function _add_history(json_) {
    time = json_['time'];
    token = json_['token'];
    text = json_['text'];
    total_price = json_['total_price'];
    raw_html = `<a class="list-group-item list-group-item-action flex-column align-items-start text-white " style="background-color:#8b9dc3;" id="${token}"><div class="d-flex w-100 justify-content-between"><h5 class="mb-1">Commande n°${token}</h5><small>${time}</small><div class="btn btn-sm btn-danger history_btn" data-id="${current_quarter}" onclick="delete_histo(${token})">Supprimer</div></div><p class="mb-1">${text}</p><small>Prix total : ${total_price} €</small></a>`;
    $('#histo').prepend(raw_html)
}

function delete_histo(token) {
    $.post({
        url: '/delete_histo/',
        data: {
            'data': String(token),
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            let elem = $('#' + String(token));
            elem.remove();
        },
        error: function(xhr, status, error) {
            //TODO : handle error in ajax request
            console.log('Cannot update the stock page', status, error);
        }
    });
}

function hide_bar(bar) {
    $(".bar" + bar.toString()).hide();
}

function show_bar(bar) {
    $(".bar" + bar.toString()).show();
}
