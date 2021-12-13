console.log('Working');

let urlString = window.location.href;
let paramString = urlString.split('?')[1];

if (urlString.split('?').length == 1 )
{
    window.location.replace("https://micro-okta.herokuapp.com/Auth?callback="+urlString);
}

let params_arr = paramString.split('&');
let pair = params_arr[0].split('=');
const myUrl='https://micro-okta.herokuapp.com/validate?session_id='+pair[1];

$.ajax({
    url: myUrl,
    type: "GET",
    dataType: "json",
    success: function (data) {
        if (data.key == 0)
        {
            window.location.replace("https://micro-okta.herokuapp.com/Auth?callback="+urlString);
        }
    }
});
