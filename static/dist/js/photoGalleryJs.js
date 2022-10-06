// Shorthand for $( document ).ready()
$(function() {
    console.log( "ready!" );

    $('#swipeboxExample').justifiedGallery({
        lastRow : 'nojustify',
        rowHeight : 100,
        rel : 'gallery2',
        margins : 1
    }).on('jg.complete', function () {
        $('.swipeboxExampleImg').swipebox();
    });
    var outerdt
    var loadIndex = 0
    $(window).scroll(function() {
        var form_data = new FormData();
        form_data.append('loadIndex', 0);
        $.ajax({
            url:"api_loadMorePhoto",
            type:"post",
            data:form_data,
            dataType: 'json',
            processData:false,
            contentType:false,
            success:function(data){
                outerdt = data
               if (data.isSuccess == true){
                   loadIndex = loadIndex + 8
                   console.log( "api_loadMorePhoto success!" );
                    console.log( $(window).scrollTop() + " " + $(window).height() + " " +  $(document).height());
                   if($(window).scrollTop() + $(window).height() == $(document).height()) {
                        console.log( "api_loadMorePhoto success2!" );
                        for (var i = 0; i < 5; i++) {
                            //console.log( "api_loadMorePhoto!!" + data.data['webContentLink']  );

                            $('#swipeboxExample').append('<a class="swipeboxExampleImg"' +
                            'href="'+ data.data[i]['webContentLink'] + '"' + '>' +
                            '<img '+
                            'src="' + data.data[i]['webContentLink'] + '"' +
                            'alt="' + data.data[i]['name'] + '"' +
                            '/>' +
                            '</a>');
                        }
                        $('#swipeboxExample').justifiedGallery('norewind');
                  }
               }else{
                   //alert("error");
               }
            },
            error:function(e){
                //alert("error", e);
            }
        })
    });

//    var images = [
//	{
//		"url" : "https://sachinchoolur.github.io/lightslider/img/cS-1.jpg",
//		"width" : 100,
//		"height" : 200
//	},
//	{
//		"url" : "https://sachinchoolur.github.io/lightslider/img/cS-2.jpg",
//		"width" : 300,
//		"height" : 400
//	},
//];

//    $('#gallery').flexPhotoGallery({
//	imageArray: images,
//	isViewImageOnClick: true
//});

});