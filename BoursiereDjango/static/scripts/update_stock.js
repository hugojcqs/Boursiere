let interval;
$(document).ready(function() {
    time_ws();
    display_ws();
});


function hide_bar(bar) {
    $(".bar" + bar.toString()).hide();
}

function show_bar(bar) {
    $(".bar" + bar.toString()).show();
}

function update_time(next_update)
{
    clearInterval(interval);
    interval = setInterval(function(){
        // Time calculations for days, hours, minutes and seconds
        var now = Math.floor(new Date().getTime() / 1000);
        var distance = next_update - now;
        var minutes = Math.floor((distance % (60 * 60)) / 60);
        var seconds = Math.floor(distance % 60);
        if(minutes <= 0 && seconds <= 0)
        {
            clearInterval(interval);
            minutes = 0;
            seconds = 0;
        }
        // Output the result in an element with id="demo"
        document.getElementById("timer").innerHTML = minutes + "m " + seconds + "s ";
    }, 1000);
}

function time_ws()
{
    var wsStart = 'ws://localhost:8000/time';
    let socket = new WebSocket(wsStart);

    socket.onmessage = function (e) {
        let data = JSON.parse(e['data']);
        let next_update = data['next_update'];

        update_time(next_update);

    };

    socket.onopen = function (e) {

    };

    socket.onerror = function (e) {

    };

    socket.onclose = function (e) {

    };
}

function display_ws(){
    var wsStart = 'ws://localhost:8000/display';
    socket = new WebSocket(wsStart);

    socket.onmessage = function (e) {
        data = JSON.parse(e['data']);
        if(data['action'] === 'update_qtt')
        {
            let id = data['id'];
            let qtt = data['qtt'];
            let beer = $('#beer_tr_' + id);
            let beer_stock = $('#beer_stock_' + id);
            if (qtt <= 0) {
                beer.hide();
            }
            else
            {
                beer.show();
            }
            beer_stock.text(qtt);
        }
        else if(data['action'] === 'update_price')
        {
            beers = JSON.parse(data['beers']);

            $('.worth').remove();

            for(var i = 0; i < beers.length; i++)
            {
                let id = beers[i]['pk'];
                let price = beers[i]['fields']['price'];
                let best_value = beers[i]['fields']['best_value'];
                let best_price = beers[i]['fields']['best_value'];
                let trend = beers[i]['fields']['trend'];

                $('#beer_price_' + id).text(price + ' €');

                let trend_elem = $('#beer_trend_image_' + id);
                trend_elem.empty();

                if (trend === 'UP') {
                    trend_elem.append(`<i class="fas fa-caret-up fa-2x" style="color: red;"></i>`);
                } else if (trend === 'EQUAL') {
                    trend_elem.append(`<i class="fas fa-caret-right fa-2x" style="color: orange;"></i>`);
                } else {
                    trend_elem.append(`<i class="fas fa-caret-down fa-2x" style="color: green;"></i>`);
                }
            }

            let best_beer = data['best_beer'];
            $('#beer_tags_' + best_beer).append(`<span class="badge badge-warning worth" style="font-size: 16px;">Meilleur prix / taule</span>`)
            let best_prices = data['best_prices'];
            for(let i = 0; i < best_prices.length; i++)
            {
                $('#beer_tags_' + best_prices[i]).append(`<span class="badge badge-success worth" style="font-size: 16px;">Meilleur prix</span>`)
            }
        }
    };

    socket.onopen = function (e) {

    };

    socket.onerror = function (e) {

    };

    socket.onclose = function (e) {

    };
}

/*
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
*



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
                trend_elem.append(`<i class="fas fa-caret-right fa-2x" style="color: orange;"></i>`);
            } else {
                trend_elem.append(`<i class="fas fa-caret-down fa-2x" style="color: green;"></i>`);
            }
        }

        console.log(beer + ' ' + String(data.data[beer]['out_of_stock']))


        if (data.data[beer]['best_price'] === true) {
            $('#beer_tags_' + beer).append(`<span class="badge badge-success worth" style="font-size: 16px;">Meilleur prix</span>`)
        }
        if (data.data[beer]['best_value'] === true) {
            $('#beer_tags_' + beer).append(`<span class="badge badge-warning worth" style="font-size: 16px;">Meilleur prix / taule</span>`)
        }

    }
}
*/