// Shorthand for $( document ).ready()
$(function() {
    console.log( "ready!" );

    $('#swipeboxExample').justifiedGallery({
        lastRow : 'nojustify',
        rowHeight : 400,
        rel : 'gallery2',
        margins : 1
    }).on('jg.complete', function () {
        $('.swipeboxExampleImg').swipebox();
    });

    var loadIndex = 0
    var lastLoadIdx = -1
    var queryCount = 4
    function loadMorePhoto(count){
        var form_data = new FormData();
        form_data.append('loadIndex', loadIndex);
        form_data.append('itemCount', count);
        console.log( "api_loadMorePhoto!!" );
        if (lastLoadIdx == loadIndex) return
        lastLoadIdx = loadIndex
        $.ajax({
        url:"api_loadMorePhoto",
        type:"post",
        data:form_data,
        dataType: 'json',
        processData:false,
        contentType:false,
        success:function(data){
            if (data.isSuccess == true){
               //console.log( "api_loadMorePhoto success!" );
                loadIndex = loadIndex + count
                console.log( "api_loadMorePhoto success2! loadIndex: " + loadIndex );
                for (var i = 0; i < data.data.length; i++) {
                    $('#swipeboxExample').append('<a class="swipeboxExampleImg"' +
                    'href="'+ data.data[i]['webContentLink'] + '"' + '>' +
                    '<img '+
                    'src="' + data.data[i]['webContentLink'] + '"' +
                    'alt="' + data.data[i]['name'] + '"' +
                    '/>' +
                    '</a>');
                }
                $('#swipeboxExample').justifiedGallery('norewind');
           }else{
               //alert("error");
           }
        },
        error:function(e){
            //alert("error", e);
        }
    })

    }

    loadMorePhoto(8)

    $(window).scroll(function() {
       if(Math.round($(window).scrollTop()) + $(window).height() >= $(document).height()) {
           loadMorePhoto(4)
        }
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