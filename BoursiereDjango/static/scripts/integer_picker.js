$( document ).ready(function() {
    console.log( "integer picker ready!" );
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

/////TODO : Verify the way that the page is updated is good enough
///// Solution bourrin
function update_stock()
{
    $.post({
        url: '/update_stock/',
                data: {
          'data': 'empty_request',
        },
        async: true,
        dataType: 'json',
        success: function(data) {
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

                    if(data.data[beer]['out_of_stock'] == true){
                      $('#beer_tr_'+beer).hide();
                    }

                }
                $('.worth').remove();
                for (var i = 0; i < data.data.worth.length; i++) {
                    let elem = $('#beer_name_'+data.data.worth[i]);
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


function start_timer(){

  var hour = document.getElementById("timer_hour").innerHTML;
  var min = document.getElementById("timer_min").innerHTML;
  var sec = document.getElementById("timer_sec").innerHTML;

  if(sec == 0){
    if(min == 0){
      if(hour == 0){
        alert("Time out !");
        window.location.reload();
        return;
      }
      hour --;
      min = 60;
      if(hour < 10) hour = "0" + hour;
    }
    min --;
    if(min < 10) min = "0" + sec;
    sec = 59;

  }else sec--;

  if (sec < 10) sec = "0" + sec;

  document.getElementById("timer_hour").innerHTML = hour;
  document.getElementById("timer_min").innerHTML = min;
  document.getElementById("timer_sec").innerHTML = sec;


  setTimeout(start_timer, 1000);

}
