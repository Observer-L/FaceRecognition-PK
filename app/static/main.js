$(function () {
    $('#submit').click(function (e) {
        e.preventDefault();
        $img_url = $('#img_url_input').val();
        if ($img_url) {
            faces = $.ajax({
                url: 'http://127.0.0.1:5000/face',
                type: 'POST',
                async: true,
                data: {
                    img_url: $img_url
                },
                timeout: 5000,
                dataType: 'json',
                success: function (jsonData) {
                    $('#pic').attr('src', $img_url);
                    bfData = formatJsonData(jsonData['BaiduAI']);
                    afData = formatJsonData(jsonData['Azure']);
                    $('.json-results').html(bfData);
                    $('.azure-results').html(afData)
                },
                error:function(xhr,textStatus){
                    console.log(textStatus)
                },
                complete:function(){
                    console.log('结束')
                }
            })
        } else {
            alert('请填入图片URL')
        }
    });

    var formatJsonData = function (jsonData) {
        template = '';
        for (var face of jsonData) {
            for (info in face) {
                faceInfo = face[info];
                str = JSON.stringify(faceInfo);

                if (typeof faceInfo === 'object') {
                    attrs = str.substr(1, str.length-2).replace(/,/g, ',<br>');
                    prettyPrintInfo = '{<br>' + attrs + '<br>}';
                    template += `<pre><span class="info">${info}</span>：${prettyPrintInfo}</pre>`;
                } else {
                    template += `<pre><span class="info">${info}</span>：${str}</pre>`;
                }

            }
            template += '<hr>'
        }

        return template
    }
});