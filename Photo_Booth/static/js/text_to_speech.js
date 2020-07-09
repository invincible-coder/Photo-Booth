var inputs = document.querySelectorAll('.box__file');
Array.prototype.forEach.call(inputs, function(input) {
    var label = input.nextElementSibling,
        labelVal = label.innerHTML;

    input.addEventListener('change', function(e) {
        var fileName = '';
        if (this.files && this.files.length > 1)
            fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}', this.files.length);
        else
            fileName = e.target.value.split('\\').pop();

        if (fileName)
            label.querySelector('span').innerHTML = fileName;
        else
            label.innerHTML = labelVal;
    });
});

var isAdvancedUpload = function() {
    var div = document.createElement('div');
    return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
}();

var $form = $('.box');
var $input = $('.box__file');
if (isAdvancedUpload) {
    $form.addClass('has-advanced-upload');

    var droppedFiles = false;

    $form.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
            e.preventDefault();
            e.stopPropagation();
        })
        .on('dragover dragenter', function() {
            $form.addClass('is-dragover');
        })
        .on('dragleave dragend drop', function() {
            $form.removeClass('is-dragover');
        })
        .on('drop', function(e) {
            droppedFiles = e.originalEvent.dataTransfer.files;
        })
        // below piece triggers submit event automatically
        .on('drop', function(e) {
            droppedFiles = e.originalEvent.dataTransfer.files;
            $form.trigger('submit');
        });
} else {
    // below piece triggers submit event automatically for browsers that do not support drag andd drop.
    $input.on('change', function(e) {
        $form.trigger('submit');
    });
}
$form.on('submit', function(e) {
    if ($form.hasClass('is-uploading')) return false;

    $form.addClass('is-uploading').removeClass('is-error');

    if (isAdvancedUpload) {
        e.preventDefault();

        var ajaxData = new FormData($form.get(0));

        if (droppedFiles) {
            $.each(droppedFiles, function(i, file) {
                ajaxData.append($input.attr('name'), file);
            });
        }

        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            data: ajaxData,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            complete: function() {
                $form.removeClass('is-uploading');
            },
            success: function(data, status, xhr) {
                $form.addClass(data.success == true ? 'is-success' : 'is-error');
                //if (!data.success) $errorMsg.text(data.error);
                if (data.success) {
                    iziToast.success({
                        title: "Success",
                        message: data.message,
                        position: "bottomRight",
                    });
                    // from here you can send the get request to get the processed files.
                } else {
                    iziToast.error({
                        title: "Error",
                        message: data.message,
                        position: "bottomRight",
                        onclosing: function() {
                            window.location.reload();
                        }
                    });
                }
            },
            error: function(xhr, status, err) {
                iziToast.info({
                    title: "Error",
                    message: "Facing server issues, contact admin if preblem persists",
                    position: "bottomRight",
                })
            }
        });
    } else {
        // ajax for legacy browsers that do not support 'drag n drop'
        var iframeName = 'uploadiframe' + new Date().getTime();
        $iframe = $('<iframe name="' + iframeName + '" style="display: none;"></iframe>');

        $('body').append($iframe);
        $form.attr('target', iframeName);

        $iframe.one('load', function() {
            var data = JSON.parse($iframe.contents().find('body').text());
            $form
                .removeClass('is-uploading')
                .addClass(data.success == true ? 'is-success' : 'is-error')
                .removeAttr('target');
            if (!data.success) $errorMsg.text(data.error);
            $form.removeAttr('target');
            $iframe.remove();
        });
    }
});