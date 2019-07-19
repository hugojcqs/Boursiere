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
    $('#progress_tip').popover({animation:true});
});


var timeout = setInterval(function(){update_stock()}, 2000);

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
            let pourcent = data.data.pourcent;

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

            $('.worth').remove();

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

                    if(data.data[beer]['out_of_stock'] == true)
                    {
                      $('#beer_name_'+beer).hide();
                    }

                    if(data.data[beer]['best_price'] == true)
                    {
                        $('#beer_name_'+beer).append(`<span class="badge badge-success worth">Best price</span>`)
                    }

                    if(data.data[beer]['best_value'] == true)
                    {
                        $('#beer_name_'+beer).append(`<span class="badge badge-warning worth">Best value</span>`)
                    }

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


/*

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
