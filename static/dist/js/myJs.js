// Shorthand for $( document ).ready()
$(function() {
    console.log( "ready!" );
//    ExportCSV
    function hideFixContentColumns(){
        $('td:nth-child(7),th:nth-child(7)').hide();
        $('td:nth-child(9),th:nth-child(9)').hide();
        $('td:nth-child(13),th:nth-child(13)').hide();
        $('td:nth-child(14),th:nth-child(14)').hide();
        $('td:nth-child(15),th:nth-child(15)').hide();
        $('td:nth-child(16),th:nth-child(16)').hide();
        $('td:nth-child(17),th:nth-child(17)').hide();
        $('td:nth-child(18),th:nth-child(18)').hide();
        $('td:nth-child(19),th:nth-child(19)').hide();
        $('td:nth-child(20),th:nth-child(20)').hide();
        $('td:nth-child(21),th:nth-child(21)').hide();
        $('td:nth-child(22),th:nth-child(22)').hide();
        $('td:nth-child(23),th:nth-child(23)').hide();
        $('td:nth-child(24),th:nth-child(24)').hide();
    }

    function showFixContentColumns(){
        $('td:nth-child(7),th:nth-child(7)').show();
        $('td:nth-child(9),th:nth-child(9)').show();
        $('td:nth-child(13),th:nth-child(13)').show();
        $('td:nth-child(14),th:nth-child(14)').show();
        $('td:nth-child(15),th:nth-child(15)').show();
        $('td:nth-child(16),th:nth-child(16)').show();
        $('td:nth-child(17),th:nth-child(17)').show();
        $('td:nth-child(18),th:nth-child(18)').show();
        $('td:nth-child(19),th:nth-child(19)').show();
        $('td:nth-child(20),th:nth-child(20)').show();
        $('td:nth-child(21),th:nth-child(21)').show();
        $('td:nth-child(22),th:nth-child(22)').show();
        $('td:nth-child(23),th:nth-child(23)').show();
        $('td:nth-child(24),th:nth-child(24)').show();
    }

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
        showFixContentColumns()
        $("table").first().table2csv(options); // default action is 'download'
        hideFixContentColumns()
    });

    $( "#test" ).on( "click", function() {
            hideFixContentColumns()

//        $('tr').each(function(){
//            console.log(this.innerText)
//            if (this.innerText.trim() === '')
//                this.remove()
//        })
    });

    $( "#openGoogleSpreadSheet" ).on( "click", function() {
        $.ajax({
                url:"api_openGoogleSpreadSheet",
                type:"post",
                dataType: 'json',
                processData:false,
                contentType:false,
                success:function(data){
                   if (data.isSuccess == true){
                       window.open(data.data, '_blank').focus();
                   }else{
                       alert("error");
                   }
                }
                ,
                error:function(e){
                        alert("error", e);
                }
        })

    });

   $( "#importDataFromGoogleSpread" ).on( "click", function() {
        $("#OrderTable").remove()
        var form= new FormData(document.getElementById("queryForm"));
        $.ajax({
                url:"api_importDataFromGoogleSpread",
                type:"post",
                data:form,
                dataType: 'json',
                processData:false,
                contentType:false,
                success:function(data){
                   if (data.isSuccess == true){
                        $("#queryResponse").append(data.data)
                   }else{
                       alert("error");
                   }
                   hideFixContentColumns()

                }
                ,
                error:function(e){
                        alert("error", e);
                }
        })});


 $( "#btnPreviewData" ).on( "click", function(){
        var form= new FormData(document.getElementById("orderForm"));
        $.ajax({
            url:"api_parseData",
            type:"post",
            data:form,
            dataType: 'json',
            processData:false,
            contentType:false,
            success:function(data){
                    if (data.shippingDate != "")
                        $("#shippingDate-input").val(data.shippingDate)
                    if (data.arrivalDate != ""){
                        var from = data.arrivalDate.split("/")
                        var f = new Date(from[0], from[1]-1, parseInt(from[2]))
                        var day = ("0" + f.getDate()).slice(-2);
                        var month = ("0" + (f.getMonth() + 1)).slice(-2);
                        var tomorrow = f.getFullYear()+"-"+(month)+"-"+(day) ;
                        $('#arrivalDate-input').val(tomorrow);
                    }
                    if (data.name != "")
                        $("#name-input").val(data.name)
                    if (data.address != "")
                        $("#address-input").val(data.address)
                    if (data.phone != "")
                        $("#phone-input").val(data.phone)
                    if (data.mPhone != "")
                        $("#mPhone-input").val(data.mPhone)
                    if (data.numbers != "")
                        $("#numbers-input").val(data.numbers)
                    if (data.arrivalTime == "2"){
                       radiobtn = document.getElementById("arriveOnAfternoon-input");
                        radiobtn.checked = true;
                    }
                    else if (data.arrivalTime == "1"){
                        radiobtn = document.getElementById("arriveTimeOnMorning-input");
                        radiobtn.checked = true;
                    }
                    if (data.paymentMethod == "2"){
                        radiobtn = document.getElementById("cashOnDelivery-input");
                        radiobtn.checked = true;
                    }
                    else if (data.paymentMethod == "1"){
                        radiobtn = document.getElementById("transfer-input");
                        radiobtn.checked = true;
                    }

                    // clear input textarea
                    //$("#orderForm > div > div:nth-child(1) > textarea").val("")
                    // reset response text
                    $("#lblAddDataResponse").text("")
            },
            error:function(e){
                    alert("error", e);
            }
        })});

$( "#btnAddNewOrder" ).on( "click", function(){
        if($("#name-input").val() == "" ){
            alert("請輸入姓名")
            return
        }

        if($("#address-input").val() == "" )
        {
            alert("請輸入地址")
            return
        }
        if($("#phone-input").val() == "" && $("#mPhone-input").val() == ""){
            alert("請輸入電話")
            return
        }


        var form= new FormData(document.getElementById("orderForm"));

        $.ajax({
            url:"api_addNewData",
            type:"post",
            data:form,
            dataType: 'json',
            processData:false,
            contentType:false,
            success:function(data){
               if (data.isSuccess == true){
                    var dt = new Date();
                    var sec = ("0" + (dt.getSeconds() + 1)).slice(-2);
                    var time = dt.getHours() + ":" + dt.getMinutes() + ":" + sec;
                   $("#lblAddDataResponse").text("新增成功: 姓名：" +$("#name-input").val() + "  (" + time + ")")
                   // reset all items.
                   $("#name-input").val("")
                   $("#address-input").val("")
                   $("#phone-input").val("")
                   $("#mPhone-input").val("")
                   $("#numbers-input").val("")
                   $("#userComment-input").val("")
                   // clear input textarea
                   $("#orderForm > div > div:nth-child(1) > textarea").val("")
                   radiobtn = document.getElementById("arriveTimeOnMorning-input");
                   radiobtn.checked = true;
                   radiobtn = document.getElementById("transfer-input");
                   radiobtn.checked = true;
               }else{
                   $("#lblAddDataResponse").text("新增失敗")
               }
            }
            ,
            error:function(e){
                    alert("error", e);
            }
        })});

// Update UI
    function updateArrivalDate(Text){
        if ($("#shippingDate-input").val()){
            var from = $("#shippingDate-input").val().split("-")
            var f = new Date(from[0], from[1]-1, parseInt(from[2])+1)
            var day = ("0" + f.getDate()).slice(-2);
            var month = ("0" + (f.getMonth() + 1)).slice(-2);
            var tomorrow = f.getFullYear()+"-"+(month)+"-"+(day) ;
            $('#arrivalDate-input').val(tomorrow);
            $('#GoogleSpreadArrivalDate-input').val(tomorrow);
        }
    }
    $("#shippingDate-input").on("input", updateArrivalDate);

    var now = new Date();
    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);
    var today = now.getFullYear()+"-"+(month)+"-"+(day) ;
    $('#shippingDate-input').val(today);
    updateArrivalDate()
});