$(document).ready(function() {
    console.log("integer picker ready!");
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
    update_stock_ajax();
});


var timeout = setInterval(function() {
    update_stock_ajax()
}, 2000);

function update_stock_ajax() {
    $.post({
        url: '/update_stock/',
        data: {
            'data': 'empty_request',
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            _update_stock(data);
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


function sound(src) {
    this.sound = document.createElement("audio");
    this.sound.src = src;
    this.sound.setAttribute("preload", "auto");
    this.sound.setAttribute("controls", "none");
    this.sound.style.display = "none";
    document.body.appendChild(this.sound);
    this.play = function() {
        this.sound.play();
    };
    this.stop = function() {
        this.sound.pause();
    };
}


function _update_stock(data) {
    let pourcent = data.data.pourcent;
    var progess = $("#progress_bar");
    let val = pourcent;
    let rounded = Math.round(val);
    let progress_tip = $('#progress_tip');
    let progress_title = $('#title_progress_bar');
    let progress_msg = $('#title_progress_bar_dynamic');
    let test = $('#utest');


    progress_tip.tooltip('update');
    progress_msg.text(" "+rounded + "%");

    progess.attr("aria-valuenow", val)
        .css("width", val + "%")
        .attr("aria-valuenow", val);
    $('.worth').remove();
    for (var beer in data.data) {

        if (data.data.hasOwnProperty(beer)) {
            $('#beer_price_' + beer).text(data.data[beer]['price'] + ' €');
            //$('#beer_stock_' + beer).text(data.data[beer]['stock']);
            $('#beer_stock_' + beer).text(data.data[beer]['stock']);
            trend_elem = $('#beer_trend_image_' + beer);
            trend_elem.empty();

            if (data.data[beer]['trend'] === 'UP') {
                trend_elem.append(`<i class="fas fa-caret-up fa-2x" style="color: red;"></i>`);
            } else if (data.data[beer]['trend'] === 'EQUAL') {
                trend_elem.append(`<i class="fas fa-caret-left fa-2x" style="color: orange;"></i>`);
            } else {
                trend_elem.append(`<i class="fas fa-caret-down fa-2x" style="color: green;"></i>`);
            }
        }

        console.log(beer + ' ' + String(data.data[beer]['out_of_stock']))
        if (data.data[beer]['out_of_stock'] === true) {
            $('#beer_tr_' + beer).hide();
        }

        if (data.data[beer]['best_price'] === true) {
            $('#beer_tags_' + beer).append(`<span class="badge badge-success worth" style="font-size: 16px;">Meilleur prix</span>`)
        }
        if (data.data[beer]['best_value'] === true) {
            $('#beer_tags_' + beer).append(`<span class="badge badge-warning worth" style="font-size: 16px;">Meilleur prix / taule</span>`)
        }

    }
}
