$(document).ready(function(){
    var token = '{{csrf_token}}';
//    the part of active ok of all data including students
    var active_grade = $('.active-grade').children('.active').attr('gp');

    $(".user_active").click(function(){
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: "/active-yes/",
            header: {'X-CSRFToken': '{{ csrf_token }}'},
            data:{
                   grade: active_grade,
            },
            type: 'GET',
            success: function(result){
             href = window.location.href
             window.open(href, '_self')
            }
        });
    });
//    archive
    $(".user_archive").click(function(){
        $.ajax({
            headers: { "X-CSRFToken": token },
             url: "/active-no/",
             header: {'X-CSRFToken': '{{ csrf_token }}'},
                data:{
                    grade: active_grade,
                },
             success: function(result){
                if(grade==100){
                     window.open('/user', '_self')
                } else {
                    href = window.location.href
                    window.open(href, '_self')
                }

            }
        });
    });

    //upload csv
    $(".upload_csv").click(function(){
        $(".input_new_group_name").hide();
        $(".upload_student_data").toggle('fast');
        $(".upload_cancel").click(function(){
            $(".upload_student_data").hide('fast');
        })
    });

    //add new group
    $(".add_new_group").click(function(){
        $(".upload_student_data").hide();
        $(".input_new_group_name").toggle('fast');

        $(".add_new_group_ok").click(function(){
            var group_name=$('input[name=new_group_name]').val();
            if (group_name==''){
                alert('Please insert the year!')
            } else{
                $.ajax({
                headers: { "X-CSRFToken": token },
                url: "/add_new_group/",
                header: {'X-CSRFToken': '{{ csrf_token }}'},
                data:{
                       group:group_name
                },
                type: 'GET',
                success: function(result){
                    if (result != group_name){
                        alert("This group is already exist")
                    } else{
                        href = window.location.href
                    window.open(href, '_self')
                    }
                }
                });
            }
        });
        $(".add_new_group_cancel").click(function(){
             $(".input_new_group_name").hide('fast');
        });
    });

    //checking is the first login in the past
//    $(".login_student_check").click(function(){
//        var text = $(this).parent().parent().prev().text()
//        if (text == 'N/A'){
//            alert("He did not log in in the past. So you do not need action!");
//            return false;
//        } else {
//            return true;
//        }
//
//    });

    $(".individual_state").click(function(){
        var text = $(this).parent().prev().text()
        var id = $(this).parent().prev().prev().prev().text()
        var state = $(this).text()
        if (state == 'Active'){
            is_act = 0;
        } else {
            is_act = 1;
        }
        if (text == 'N/A'){
            alert("He did not log in in the past. So you do not need action!");
        } else {
            $.ajax({
                url: "/active-archive/",
                header: {'X-CSRFToken': '{{ csrf_token }}'},
                data:{
                       id:id,
                       state:is_act
                },
                type: 'GET',
                success: function(result){
                    href = window.location.href
                    window.open(href, '_self')
                }
            });
        }
    });

});