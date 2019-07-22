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

play_sound();
get_next_update_and_play();

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function get_timestamp() {
    return Date.now() / 1000;
}

function get_next_update_and_play()
{
    $.post({
        url: '/sound_ajax/',
        data: {
          'data': 'none'
        },
        async: true,
        dataType: 'json',
        success: function (data) {
            time_to_update = data.next_update - get_timestamp();
            if(time_to_update > 0)
            {
                console.log(time_to_update);
                setTimeout(play_sound, time_to_update * 1000 - 500);
            }
            else
            {
                console.log("Negative time, will try to get the time in 20 seconds.");
                setTimeout(get_next_update_and_play, 20 * 1000);
            }
        }
    });
}

async function play_sound()
{
    let audio = new Audio(document.location.origin + '/static/sounds/sound.mp3');
    audio.play();
    await sleep(10000);
}