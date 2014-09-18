var user;
var res;
function initialize(){


$("#message").submit(function(){

    if (res.status==="connected"){
    $("#message [name='access_token']").val(user.accessToken);
    $("#message [name='facebookid']").val(user.userID);
    }
    else {
      alert("Please Log in to facebook");
      return false;
    }
    })

$("#message2").submit(function(){
    if (res.status==="connected"){
    $("#message2 [name='access_token1']").val(user.accessToken);
    $("#message2 [name='facebookid1']").val(user.userID);
    $("#message2 [name='msg1']").val($("#message [name='msg']").val());
    }
    else {
      alert("Please Log in to facebook");
      return false;
    }
    })
}
function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    res = response;
    user = response.authResponse;
  }
  /*function post(asd){
    var baseUrl = "https://graph.facebook.com/v2.1/";
    var url = baseUrl + asd.userID + "/feed/";
    var msg = $("#message textarea").val();
        var data = {
                    method: "post",
                    message: msg,
                    access_token: asd.accessToken
                };
        $.get(url,data,function(response){
                    if(response.id){
                        alert('Post Successful');
                        var msg = $("#message textarea").val("");
                    }else{
                        alert('An error occured. Try to reload the page and try again.')
                    }
                }); 
    }*/

  function login(){
    location.reload();
  }



  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }

  window.fbAsyncInit = function() {
  FB.init({
    appId      : '636107513170917',
    cookie     : true,   
                        
    xfbml      : true,  
    version    : 'v2.1' 
  });


  initialize();
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });


  };


  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));
