$(document).ready(function () {

    /* $('#SELECT_FILE').change( function () {
        var Input = $(this)[0];
        var File = Input.files[0];
        var Reader = new FileReader();
        Reader.onloadend = function () {
            var FileData = {
                Name: File.name,
                Content: arrayBufferToBase64(Reader.result)
            };
            Object.SelectFile(JSON.stringify(FileData));
        };
        Reader.readAsArrayBuffer(File);
    }) */

    /* function arrayBufferToBase64(buffer) {
        var binary = '';
        var bytes = new Uint8Array(buffer);
        var len = bytes.byteLength;
        for (var i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return btoa(binary);
    } */

    $('#SELECT_FILE').change(function () {
        Loading_Show();
        var Input = $(this)[0];
        var Form = new FormData();
        Form.append('File', Input.files[0]);
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5023/UploadFile',
            contentType: "application/json;charset=UTF-8",
            data: Form,
            processData: false,
            contentType: false,
            success: function (Data) {
                Loading_Hide();
                if (Data !== 'Verify') {
                    QueryWindow(Data.Title, Data.Info);
                    $('#WIN-NEXT').click(function () {
                        Loading_Show();
                        HideWindow();
                        var File = Input.files[0];
                        var Data = { FileName: File.name };
                        $.ajax({
                            type: 'POST',
                            url: 'http://127.0.0.1:5023/ConfirmUpload',
                            contentType: "application/json;charset=UTF-8",
                            data: JSON.stringify(Data),
                            success: function (Data) {
                                setTimeout( function () {
                                    Loading_Hide();
                                    InfoWindow(Data.Title, Data.Info);
                                    $('#CLS_W').click(function () {
                                        HideWindow();
                                    })
                                }, 530)
                            }
                        })
                    })
                }
                $('#CLS_W').click(function () {
                    HideWindow();
                })
            },
        })
    })

    $('#AUTO_INSTAL').click(function () {
        Loading_Show();
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5023/AutoInstal',
            contentType: 'json',
            success: function (Data) {
                Loading_Hide();
                InfoWindow(Data.Title, Data.Info);
                $('#CLS_W').click(function () {
                    HideWindow();
                })
            }
        })
    })

    function Loading_Show () {
        var Loading = $('.UI-Loading');
        Loading.css('animation', 'LOADING-SHOW 1s forwards');
    }

    function Loading_Hide () {
        var Loading = $('.UI-Loading');
        Loading.css('animation', 'LOADING-HIDE 1s forwards');
    }

    function QueryWindow (Title, Info) {
        if (Info) {
            HTML = 
            '<div class="UI-Window_BG"></div>' +
            '<div class="UI-Window">' +
            '<div class="UI-Window_content">' +
            '<div class="UI-Window_title">' + Title + '</div>' +
            '<div class="UI-Window_text">' + Info + '</div>' +
            '</div>' +
            '<div class="UI-Window_BTNS">' +
            '<button id="WIN-NEXT" class="UI-Window_button">Далее</button>' +
            '<div class="UI-Window_BW"></div>' +
            '<button id="CLS_W" class="UI-Window_BTN_NOACT UI-Window_button">Отменить</button>' +
            '</div>' +
            '</div>';

            $("body").append(HTML);

            $(".UI-Window_BG").css({ animation: "0.6s forwards WINDOW-SHOW_BG" });
            $(".UI-Window").css({ animation: "0.4s forwards WINDOW-SHOW" });
        }
    }

    function InfoWindow (Title, Info) {
        if (Info) {
            HTML =
            '<div class="UI-Window_BG"></div>' +
            '<div class="UI-Window">' +
            '<div class="UI-Window_content">' +
            '<div class="UI-Window_title">' + Title + '</div>' +
            '<div class="UI-Window_text">' + Info + '</div>' +
            '</div>' +
            '<div class="UI-Window_BTNS">' +
            '<button class="UI-Window_button" id="CLS_W">Хорошо</button>' +
            '</div>' +
            '</div>';

            $("body").append(HTML);

            $(".UI-Window_BG").css({ animation: "0.6s forwards WINDOW-SHOW_BG" });
            $(".UI-Window").css({ animation: "0.4s forwards WINDOW-SHOW" });
        }
    }

    function HideWindow() {
        $(".UI-Window_BG").css({ animation: "0.6s forwards WINDOW-HIDE_BG" });
        $(".UI-Window").css({ animation: "0.4s forwards WINDOW-HIDE" });
        setTimeout(function () {
            $(".UI-Window_BG").remove();
            $(".UI-Window").remove();
        }, 520);
    }

})