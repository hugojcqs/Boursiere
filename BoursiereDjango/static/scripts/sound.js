$(document).ready(function() {
    var wsStart = 'ws://localhost:8000/sound';
    socket = new WebSocket(wsStart);

    socket.onmessage = function (e) {
        data = JSON.parse(e['data']);
        if(data['action'] === 'update_qtt')
        {
            console.log(data);
        }
        else if(data['action'] === 'update_price')
        {
            console.log(data);
        }
        else if(data['action'] === 'play_sound')
        {
            console.log(data);
        }
    };

    socket.onopen = function (e) {
        console.log("open", e)
    };

    socket.onerror = function (e) {
        console.log("error", e)
    };

    socket.onclose = function (e) {
        console.log("close", e)
    };
});

async function play_sound() {
    let audio = new Audio(document.location.origin + '/static/sounds/sound.mp3');
    audio.play();
}