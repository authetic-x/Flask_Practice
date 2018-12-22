$(document).ready(function () {
     var ENTER_KEY = 13;

     $(document).ajaxError(function (event, request) {
        var message = null;

        if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
            message = request.responseJSON.message;
        } else if (request.responseText) {
            var IS_JSON = true;
            try {
                var data = JSON.parse(request.responseText);
            }
            catch (err) {
                IS_JSON = false;
            }

            if (IS_JSON && data !== undefined && data.hasOwnProperty('message')) {
                message = JSON.parse(request.responseText).message;
            } else {
                message = default_error_message;
            }
        } else {
            message = default_error_message;
        }
        M.toast({html: message});
    });

    $(window).bind("hashchange", function () {
        var hash = window.location.hash.replace('#', '');
        var url = null;
        if (hash === 'login') {
            url = login_page_url;
        } else if (hash === 'app') {
            url = app_page_url
        } else {
            url = intro_page_url
        }

        $.ajax({
            type: 'GET',
            url: url,
            success: function (data) {
                $("#main").hide().html(data).fadeIn(800);
                activeM();
            }
        });
    });

    if (window.location.hash === '') {
        window.location.hash = '#intro';
    } else {
        $(window).trigger("hashchange");
    }

    $(document).on('click', '#register-btn', function () {
        $.ajax({
            type: 'GET',
            url: register_url,
            success: function (data) {
                $('#username-input').val(data.username);
                $('#password-input').val(data.password);
                M.toast({html: data.message});
            }
        });
    });

    function login_user() {
        username = $('#username-input').val();
        password = $('#password-input').val();
        if (!username || !password) {
            M.toast({html:'Login error'});
            return;
        }
        data = {
            'username':username,
            'password':password
        };
        $.ajax({
            type: "POST",
            url: login_url,
            data: JSON.stringify(data),
            contentType: 'application/json,charset=UTF-8',
            success: function (data) {
                if (window.location.hash === '#app' || window.location.hash === 'app') {
                    $(window).trigger('hashchange');
                } else {
                    window.location.hash = '#app';
                }
                activeM();
                M.toast({html: data.message});
            }
        });
    }
    $('.login-input').on('keyup', function (e) {
       if (e.which === ENTER_KEY) {
           login_user();
       }
    });
    $(document).on('click', '#login-btn', login_user);

    $(document).on('click', '#logout', function () {
        $.ajax({
            type: 'GET',
            url: logout_url,
            success: function (data) {
                window.location.hash = 'intro';
                activeM();
                M.toast({html:data.message});
            }
        });
    });

    $(document).on('mouseenter', '.item', function () {
       $(this).find('.edit-btns').removeClass('hide');
    });
    $(document).on('mouseleave', '.item', function () {
       $(this).find('.edit-btns').addClass('hide');
    });

    function refresh_count() {
        var $items = $('.item');
        display_dashboard();
        var all_count = $items.length;
        var active_count = $items.filter(function () {
            return $(this).data('done') === false;
        }).length;
        var completed_count = $items.filter(function () {
            return $(this).data('done') === true;
        }).length;
        $('#all_count').html(all_count);
        $('#active_count').html(active_count);
        $('#completed_count').html(completed_count);
    }

    $(document).on('keyup', '#item-input', new_item.bind(this));

    function new_item(e) {
        var $input = $('#item-input');
        var value = $input.val.trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $input.focus().val('');
        $.ajax({
            type: 'POST',
            url: new_item_url,
            data: JSON.stringify({'body':value}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                M.toast({html:data, classes:'rounded'});
                $('.items').append(data.html);
                activeM();
                refresh_count();
            }
        });
    }

    $(document).on('click', '#active_item', function () {
        var $input = $('#item-input');
        var $items = $('.item');
        $input.focus();
        $items.show();
        $item.filter(function () {
            return $(this).data('done') === true;
        }).hide();
    });

    $(document).on('click', '#all_item', function () {
        $('#item-input').focus();
        $('.item').show();
    });

    $(document).on('click', '#done_item', function () {
        $('#item-input').focus();
        var $items = $('.item');
        $items.show();
        $items.filter(function () {
            return $(this).data('done') === false;
        }).hide();
    });

    $(document).on('click', '.done-btn', function () {
        $('#item-input').focus();
        $item = $(this).parent().parent();
        $this = $(this);

        if ($item.data('done') === false) {
            $.ajax({
               type: 'PATCH',
               url: $this.data('href'),
               success: function (data) {
                    $item.next().removeClass('active_item');
                    $item.next().addClass('inactive_item');
                    $this.find('i').text('check_box_outline_blank');
                    $item.data('done', true);
                    M.toast({html:data.message});
                    refresh_count();
               }
            });
        } else {
            $.ajax({
               type: 'PATCH',
               url: $this.data('href'),
               success: function (data) {
                    $item.next().removeClass('inactive_item');
                    $item.next().addClass('active_item');
                    $this.find('i').text('check_box');
                    $item.data('done', false);
                    M.toast({html:data.message});
                    refresh_count();
               }
            });
        }
    });

    function display_dashboard() {
        var all_count = $('.item').length;
        if (all_count === 0) {
            $('#dashboard').hide();
        } else {
            $('#dashboard').show();
            $('ul.tabs').tabs();
        }
    }
    function activeM() {
        $('.sidenav').sidenav();
        $('ul.tabs').tabs();
        $('.modal').modal();
        $('.tooltipped').tooltip();
        $('.dropdown-trigger').dropdown({
                constrainWidth: false,
                coverTrigger: false
            }
        );
        display_dashboard();
    }
    activeM();
});

