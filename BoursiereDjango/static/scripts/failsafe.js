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

if($('#statut').text() === 'True')
{
    var timeout = setInterval(function(){update_page()}, 3000);
}
});


function activate_fail_safe()
{

    $.post({
        url: '/activate_failsafe/',
                data: {
          'data': String($('#failsafe_password').val()),
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            $('#statut').text('True');
        }
      });
    if($('#statut').text() === 'True')
    {
        var timeout = setInterval(function(){update_page()}, 500);
    }
}

function _build_db()
{
    let db = [];
    $(".price").each(function() {
        beer = $(this);
        db.push([beer.attr('id'), beer.text()])
});
    return db;
}



function update_page()
{
            $.post({
        url: '/timer_to_next_up/',
                data: {
          'data': 'empty_request',
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            let pourcent = data.pourcent;

            var progess = $("#progress_bar");
            let val = pourcent;
            let rounded = Math.round(val);
            let progress_tip = $('#progress_tip');
            progress_tip.tooltip('update');
            if(rounded < 97 && rounded > 8)
            {
                progress_tip.text(rounded + " %");
            }
            else
            {
                progress_tip.text("");
            }

            progess.attr("aria-valuenow", val)
            .css("width", val + "%")
            .attr("aria-valuenow", val);

            if(data.time_remaining < 5)
            {
                set_price();
            }
        }
      });
}

function set_price()
{
        $.post({
        url: '/update_price_failsafe/',
                data: {'new_prices':JSON.stringify(_build_db())},
        async: true,
        dataType: 'json',
        success: function(data) {
            console.log('Success')
        }
      });
}
