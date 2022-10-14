// Shorthand for $( document ).ready()
$(function() {
    console.log( "ready!" );

    $('#swipeboxExample').justifiedGallery({
        lastRow : 'nojustify',
        rowHeight : 400,
        rel : 'gallery2',
        margins : 1
    }).on('jg.complete', function () {
        $('.swipeboxExampleImg').swipebox({
//            nextSlide:function(idx){
//                if (idx == $('.swipeboxExampleImg').length - 1 ){
//                    console.log("load more photo" + idx)
//                    loadMorePhoto(4, function(){
//                        console.log("loadComplete")
//                        $.swipebox.plugin().init()
//
//
//                    })
//                }
//                console.log("nextslide" + idx)
//            }
        });
    });

    function shuffle(){
        $.ajax({
                url:"api_shufflePhoto",
                type:"post",
                dataType: 'json',
                processData:false,
                contentType:false,
                success:function(data){

                }
                ,
                error:function(e){
                }
        })
    }
    shuffle()

    var loadIndex = 0
    var lastLoadIdx = -1
    var queryCount = 4
    function loadMorePhoto(count){
        var form_data = new FormData();
        form_data.append('loadIndex', loadIndex);
        form_data.append('itemCount', count);
        //console.log( "api_loadMorePhoto!!" );
        if (lastLoadIdx == loadIndex) return
        lastLoadIdx = loadIndex
        console.log("load photo : " + count )

        $.ajax({
            url:"api_loadMorePhoto",
            type:"post",
            data:form_data,
            dataType: 'json',
            processData:false,
            contentType:false,
            success:function(data){
                if (data.isSuccess == true){
                   console.log( "api_loadMorePhoto success!" );
                    loadIndex = loadIndex + count
                   // console.log( "api_loadMorePhoto success2! loadIndex: " + loadIndex );
                    var counter = Math.floor(Math.random() * 200)
                    for (var i = 0; i < data.data.length; i++) {
                        var wck = data.data[i]['webContentLink']
                        var name = data.data[i]['name'];

                        (function(wck, name, counter){
                            window.setTimeout(function() {
                               // console.log("load photo in : " + counter )
                                //console.log("load photo in : " + name )
                                 $('#swipeboxExample').append('<a class="swipeboxExampleImg"' +
                                    'href="'+ wck + '"' + '>' +
                                    '<img '+
                                    'src="' + wck + '"' +
                                    'alt="' + name + '"' +
                                    '/>' +
                                    '</a>');
                                    $('#swipeboxExample').justifiedGallery('norewind');
                                }, counter);
                          })(wck, name, counter);

                        counter = counter + Math.floor(Math.random() * 5000)
                    }

    //                if (onLoadComplete != null){
    //                    onLoadComplete()
    //                }
               }else{
                   //alert("error");
               }
            },
            error:function(e){
                //alert("error", e);
            }
        })
    }

    loadMorePhoto(Math.floor(Math.random() * 4) + 5)

    $(window).scroll(function() {
       if(Math.round($(window).scrollTop()) + $(window).height() + 300 >= $(document).height()) {
           // random load 4 ~ 7

           loadMorePhoto(Math.floor(Math.random() * 4) + 2)
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