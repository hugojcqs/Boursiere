$( document ).ready(function() {
    console.log( "ready!" );
});

function plus(i)
{
    let input = $("#input" + i.toString());
    let new_v_input = Number(input.val()) + 1;
    input.val(new_v_input);
}

function minus(i)
{
    let input = $("#input" + i.toString());
    let new_v_input = Number(input.val()) - 1;
    input.val(new_v_input);
}