$( document ).ready(function() {
    console.log( "ready!" );
});

var db = {};

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

});


function calculate_price()
{
    console.log(JSON.stringify(db));
    $.post({
        url: '/calculate_price/',
        data: {
          'data': JSON.stringify(db)
        },
        async: true,
        dataType: 'json',
        success: function (data) {
            let elem = $("#total_price");
            elem.text('Prix : '+ String(data['price']) + " €");
        }
      });
}

function make_order()
{
    $.post({
        url: '/make_order/',
        data: {
          'data': JSON.stringify(db)
        },
        async: true,
        dataType: 'json',
        success: function (data) {
                _add_history(data);
                $(".input-number").val(0);
                $("#total_price").text('Prix : 0 €');
                db = {}
        }
      });
}

function plus(i, beer_name)
{
    let input = $("#input" + i.toString());
    let new_v_input = Number(input.val()) + 1;
    input.val(new_v_input);
    db[beer_name] = new_v_input;
    calculate_price();
}

function minus(i, beer_name)
{
    let input = $("#input" + i.toString());
    let new_v_input = Number(input.val()) - 1;
    input.val(new_v_input);
    db[beer_name] = new_v_input;
    calculate_price();
}

function _add_history(json_) {
    time = json_['time'];
    token = json_['token'];
    text = json_['text'];
    total_price = json_['total_price'];
    raw_html = `<a class="list-group-item list-group-item-action flex-column align-items-start text-white bg-secondary" id="${token}"><div class="d-flex w-100 justify-content-between"><h5 class="mb-1">Commande n°${token}</h5><div class="btn-sm btn-danger" onclick="delete_histo(${token})">Supprimer</div></div><p class="mb-1">${text}</p><small>Prix total : ${total_price}</small></a>`;
    $('#histo').prepend(raw_html)
}

function delete_histo(token){
        console.log(token);
        $.post({
        url: '/delete_histo/',
        data: {
          'data': token,
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            let elem = $('#'+String(token));
            elem.remove();
        }
      });
}