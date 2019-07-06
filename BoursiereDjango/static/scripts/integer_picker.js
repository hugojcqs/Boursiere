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

setInterval(function(){ update_stock(); }, 5000);

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
    raw_html = `<a class="list-group-item list-group-item-action flex-column align-items-start text-white bg-secondary" id="${token}"><div class="d-flex w-100 justify-content-between"><h5 class="mb-1">Commande n°${token}</h5><small>${time}</small><div class="btn-sm btn-danger" onclick="delete_histo(${token})">Supprimer</div></div><p class="mb-1">${text}</p><small>Prix total : ${total_price} €</small></a>`;
    $('#histo').prepend(raw_html)
}

function delete_histo(token){
        console.log(token);
        $.post({
        url: '/delete_histo/',
        data: {
          'data': String(token),
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            let elem = $('#'+String(token));
            elem.remove();
        }
      });
}


function update_stock()
{
    console.log('Update stock');
    $.post({
        url: '/update_stock/',
                data: {
          'data': 'empty_request',
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            console.log(data.data);
                for(var beer in data.data){

                    if (data.data.hasOwnProperty(beer)) {
                    $('#beer_price_'+beer).text(data.data[beer]['price'] + ' €');
                    $('#beer_stock_'+beer).text(data.data[beer]['stock']);
                    trend_elem = $('#beer_trend_image_'+beer);
                    trend_elem.empty();
                    if(data.data[beer]['trend'] == 'UP')
                    {
                        trend_elem.append(`<i class="fas fa-caret-up fa-2x" style="color: red;"></i>`);
                    }
                    else if(data.data[beer]['trend'] == 'EQUAL')
                    {
                        trend_elem.append(`<i class="fas fa-caret-left fa-2x" style="color: orange;"></i>`);
                    }
                    else
                    {
                        trend_elem.append(`<i class="fas fa-caret-down fa-2x" style="color: green;"></i>`);
                    }
                    }

                }
                $('.worth').remove();
                 console.log(data.data.worth.length);
                for (var i = 0; i < data.data.worth.length; i++) {
                    let elem = $('#beer_name_'+data.data.worth[i]);
                    console.log(elem);
                     elem.append(`<span class="badge badge-success worth">worth</span>`);
                    // ...
                }
        }
      });
}

function hide_bar(bar)
{
    $(".bar"+bar.toString()).hide();
}

function show_bar(bar)
{
    $(".bar"+bar.toString()).show();
}
