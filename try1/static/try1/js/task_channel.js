$(function () {
    let $form = $('form#form');
    var $answer_el;
    var $btn_answer = $('button.answer');
    socket.onmessage = function (event) {
        var obj = jQuery.parseJSON(event.data);
        if (obj.over === true) {
            $form.submit();

        } else {
            $('.form_container').html(obj.form_block);
        }
    };

    ;
    $btn_answer.on('click', function () {
        let input_type = $("input[name='question']").attr('type');
        if (input_type === 'text') {
            $answer_el = $("input[name='question']");
        } else {
            $answer_el = $("input[name='question']:checked");
        }
        var question_body = $('div.question_body').text();
        let validator = $form.validate({
            rules: {

                question: {
                    equalTo: question_body,
                }
            },
            errorPlacement: function (error, element) {
                if (element.attr("name") === "question") {
                    error.appendTo(".otree-modal-message");
                }
            }
        });
        if (validator.form() === true) {
            let answer = $answer_el.val();

            let task_id = $answer_el.data('task');
            var msg = {
                'answer': answer,
                'task_id': task_id,
            };
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify(msg));
            }
            ;
        } else {
            $('#error_modal').modal('show');
        }
        ;
        validator.destroy();

    });
    $form.keydown(function (e) {
        if (e.keyCode == 13) {
            if (event.keyCode === 13) {
                event.preventDefault();
                $btn_answer.click();
                return false;
            }
        }
    });

});