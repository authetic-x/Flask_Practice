$(document).on('ready', function () {

    var ENTER_KEY = 13;
    $(document).on('keyup', '#item-input', new_item.bind(this));

    function new_item(e) {
        var $input = $('#item-input');
        var value = $input.val().trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $input.focus().val('');
        $.ajax({
            type:'POST',
            url:new_item_url,
            data:JSON.stringify({'body':value}),
            contentType:'application/json;charset=UTF-8',
            success:function (data) {
                M.toast({html: data.message, classes:'rounded'});
                $('.items').append(data.html);
                activeM();
                refresh_count();
            }
        });
    }

    $(window).bind("hashchange", function () {
        var hash = window.location.hash.replace('#', '');
        var url = null;
        if (hash === 'login') {
            url = login_page_url;
        } else if (hash === 'app') {
            url = app_page_url;
        } else {
            url = intro_page_url;
        }

        $.ajax({
            type: 'GET',
            url: url,
            success: function (data) {
                $('#main').hide().html(data).fadeIn(800);
                activeM();
            }
        });
    });

    if (window.location.hash === '') {
        window.location.hash = '#intro';

    }
    $(window).trigger("hashchange");

    function register() {
        $.ajax({
            type:'GET',
            url:register_url,
            success:function (data) {
                $('#username-input').val(data.username);
                $('#password-input').val(data.password);
                M.toast({html: data.message})
            }
        })
    }

    $(document).on('click', '#register-btn', register);
    
    function activeM() {
        
    }
    
    function refresh_count() {
        
    }
});