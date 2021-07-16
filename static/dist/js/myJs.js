// Shorthand for $( document ).ready()
$(function() {
    console.log( "ready!" );
//    ExportCSV
    $( "#exportCSV" ).on( "click", function() {
        var now = new Date();
        var day = ("0" + now.getDate()).slice(-2);
        var month = ("0" + (now.getMonth() + 1)).slice(-2);
//        var hour = ("0" + (now.getHours() + 1)).slice(-2);
//        var minute = ("0" + (now.getMinutes() + 1)).slice(-2);
        var time = now.get
        var today = now.getFullYear()+(month)+(day);//+(hour)+(minute);
        let options = {
        "separator": ",",
        "newline": "\n",
        "quoteFields": false,
        "excludeColumns": "",
        "excludeRows": "",
        "trimContent": true,
        "filename": today + "葡萄訂單.csv",
        "appendTo": "#output"
        }
      $("table").first().table2csv(options); // default action is 'download'
    });

    $( "#test" ).on( "click", function() {
//        $('tr').each(function{
//
//            this.remove()
//        })
//
//        $("td").each(function() {
//        if (this.innerText === '') {

//            this.closest('tr').remove();
//        })
        $('tr').each(function(){
            console.log(this.innerText)
            if (this.innerText.trim() === '')
                this.remove()
        })
    });
//    });




// Update UI
    function updateArrivalDate(Text){
      var from = $("#shippingDate-input").val().split("-")
        var f = new Date(from[0], from[1]-1, parseInt(from[2])+1)
        var day = ("0" + f.getDate()).slice(-2);
        var month = ("0" + (f.getMonth() + 1)).slice(-2);
        var tomorrow = f.getFullYear()+"-"+(month)+"-"+(day) ;
        $('#arrivalDate-input').val(tomorrow);
    }
    $("#shippingDate-input").on("input", updateArrivalDate);

    var now = new Date();
    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);
    var today = now.getFullYear()+"-"+(month)+"-"+(day) ;
    $('#shippingDate-input').val(today);
    updateArrivalDate()
});