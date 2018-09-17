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
                    data = formatJsonData(jsonData);
                    $('.json-results').html(data)
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
    })
    
    var formatJsonData = function (jsonData) {
        template = '';
        for (var face of jsonData) {
            for (info in face) {
                template += `<pre><span class="info">${info}</span>：${JSON.stringify(face[info])}</pre>`;
                console.log(info, face[info])
            }
            template += '<hr>'
        }

        return template
    }
});