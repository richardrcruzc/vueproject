var EXAMNO_STR = "examno_str";


function init_examno_cookie(paramval){

    if(paramval== "NO_PARAM"){
        setCookie(EXAMNO_STR, "");
    }else{
        var str = getCookie(EXAMNO_STR);
        var arr = str.split(',');

        for(var i = 0; i <arr.length; i++) {
            var no = arr[i];
            $('input[name="q_id"][value="'+no+'"]').prop("checked", true);
        }
    }
}

function add_check_examno(examno){
    //document.cookie = cname + "=" + cvalue+ ";" + ";path=/test_list/";
    var retstr = getCookie(EXAMNO_STR);

    retstr += ( retstr=="" ? "" : "," )  + examno;

    setCookie(EXAMNO_STR, retstr);
}

function remove_check_examno(examno){
    var str = getCookie(EXAMNO_STR);
    var arr = str.split(',');
    var retstr = "";

    for(var i = 0; i <arr.length; i++) {
        var no = arr[i];
        if(no != examno){
            retstr += ( retstr=="" ? "" : "," )  + no;
        }
    }

    setCookie(EXAMNO_STR, retstr);
}


$(".selecting").change(function(){
    var check_obj = $(this).children('input[name="q_id"]');

    var question_id = check_obj.val();

    if(check_obj.prop('checked') == true){
        add_check_examno(question_id);
    }else{
        remove_check_examno(question_id);
    }

});



function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function setCookie(cname, cvalue/*, exdays*/) {
   document.cookie = cname + "=" + cvalue + ";path=/";

//  var d = new Date();
//  d.setTime(d.getTime() + (exdays*24*60*60*1000));
//  var expires = "expires="+ d.toUTCString();
//  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }

    return "NO_PARAM";
};

$(".activate").click(function(){
    var act = 1;
    $.ajax({
        url: "/activate-test/",
        header: {'X-CSRFToken': '{{ csrf_token }}'},
        data:{
            act: act,
        },
        type: 'GET',
        success: function(result){
            alert("The final test is activated!")
        }
    });
});

$(".deactivate").click(function(){
    var act = 0;
    $.ajax({
        url: "/activate-test/",
        header: {'X-CSRFToken': '{{ csrf_token }}'},
        data:{
            act: act,
        },
        type: 'GET',
        success: function(result){
            alert("The final test is deactivated!")
        }
    });
});


$(function(){

    init_examno_cookie(getUrlParameter('page'));

})