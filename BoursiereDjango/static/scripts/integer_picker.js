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
    $.post({
        url: '/calculate_price/',
        data: {
          'json_': JSON.stringify(db)
        },
        async: false,
        dataType: 'json',
        success: function (price) {
            $("#total_price").val('Prix total : '+ String(price));
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