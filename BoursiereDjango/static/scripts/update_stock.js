$( document ).ready(function() {
    console.log( "integer picker ready!" );
});

var db = {};

/////TODO : Verify the way that the page is updated is good enough
///// Solution bourrin
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
    update_stock();
});



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
            var eta_ms = data.data.next_update - new Date().getTime() / 1000;
            if(eta_ms <= 0)
                eta_ms = 1;
            console.log(data.data.next_update);
            console.log('Will updated in ');
            console.log(eta_ms);
            var timeout = setTimeout(function(){update_stock()}, eta_ms*1000);

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

                //update progress bar TODO: isolate this

              //  $('#progress_tip').val($('.progress').val()+5);
              //  $('#progress_tip').tooltip('update');
              //  $('#progress_tip').attr('title', $('.progress').val());
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

function kill_update_price(){
    $.post({
    url: '/kill_process/',
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


/*
>>>>>>> 378b7dbfe179c03e33052714c56025aa386eb343:BoursiereDjango/static/scripts/update_stock.js
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

 */