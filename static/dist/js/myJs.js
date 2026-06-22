// Shorthand for $( document ).ready()
$(function() {
    console.log( "ready!" );

    // Display column indices (1-based) from OrderTable, in desired screen order:
    // 姓名(1), 件數(6), 電話(2), 手機(3), 地址(4), 代收金額(5), 備註(8), 希望配達時間(10), 出貨日期(11), 預定配達日期(12)
    var DISPLAY_COLS = [1, 6, 2, 3, 4, 5, 8, 10, 11, 12];

    function buildDisplayTable() {
        $('#DisplayTable').remove();
        var $src = $('table#OrderTable');
        if ($src.length === 0) return;

        var $display = $('<table id="DisplayTable" class="table table-hover table-bordered"></table>');
        $src.find('tr').each(function() {
            var $tr = $('<tr></tr>');
            var $cells = $(this).find('th, td');
            DISPLAY_COLS.forEach(function(colIdx) {
                $tr.append($cells.eq(colIdx - 1).clone());
            });
            $display.append($tr);
        });

        $src.hide();
        $('#queryResponse').append($display);
    }

//    CSV export: temporarily reveal hidden OrderTable with all 24 columns, export, then re-hide
    function hideFixContentColumns(){
        $('table#OrderTable td:nth-child(7),table#OrderTable th:nth-child(7)').hide();
        $('table#OrderTable td:nth-child(9),table#OrderTable th:nth-child(9)').hide();
        $('table#OrderTable td:nth-child(13),table#OrderTable th:nth-child(13)').hide();
        $('table#OrderTable td:nth-child(14),table#OrderTable th:nth-child(14)').hide();
        $('table#OrderTable td:nth-child(15),table#OrderTable th:nth-child(15)').hide();
        $('table#OrderTable td:nth-child(16),table#OrderTable th:nth-child(16)').hide();
        $('table#OrderTable td:nth-child(17),table#OrderTable th:nth-child(17)').hide();
        $('table#OrderTable td:nth-child(18),table#OrderTable th:nth-child(18)').hide();
        $('table#OrderTable td:nth-child(19),table#OrderTable th:nth-child(19)').hide();
        $('table#OrderTable td:nth-child(20),table#OrderTable th:nth-child(20)').hide();
        $('table#OrderTable td:nth-child(21),table#OrderTable th:nth-child(21)').hide();
        $('table#OrderTable td:nth-child(22),table#OrderTable th:nth-child(22)').hide();
        $('table#OrderTable td:nth-child(23),table#OrderTable th:nth-child(23)').hide();
        $('table#OrderTable td:nth-child(24),table#OrderTable th:nth-child(24)').hide();
    }

    function showFixContentColumns(){
        $('table#OrderTable td:nth-child(7),table#OrderTable th:nth-child(7)').show();
        $('table#OrderTable td:nth-child(9),table#OrderTable th:nth-child(9)').show();
        $('table#OrderTable td:nth-child(13),table#OrderTable th:nth-child(13)').show();
        $('table#OrderTable td:nth-child(14),table#OrderTable th:nth-child(14)').show();
        $('table#OrderTable td:nth-child(15),table#OrderTable th:nth-child(15)').show();
        $('table#OrderTable td:nth-child(16),table#OrderTable th:nth-child(16)').show();
        $('table#OrderTable td:nth-child(17),table#OrderTable th:nth-child(17)').show();
        $('table#OrderTable td:nth-child(18),table#OrderTable th:nth-child(18)').show();
        $('table#OrderTable td:nth-child(19),table#OrderTable th:nth-child(19)').show();
        $('table#OrderTable td:nth-child(20),table#OrderTable th:nth-child(20)').show();
        $('table#OrderTable td:nth-child(21),table#OrderTable th:nth-child(21)').show();
        $('table#OrderTable td:nth-child(22),table#OrderTable th:nth-child(22)').show();
        $('table#OrderTable td:nth-child(23),table#OrderTable th:nth-child(23)').show();
        $('table#OrderTable td:nth-child(24),table#OrderTable th:nth-child(24)').show();
    }

    $( "#exportCSV" ).on( "click", function() {
        var inputDate = new Date($('#GoogleSpreadShippingDate-input > input').val());
        var day = ("0" + inputDate.getDate()).slice(-2);
        var month = ("0" + (inputDate.getMonth() + 1)).slice(-2);
//        var hour = ("0" + (now.getHours() + 1)).slice(-2);
//        var minute = ("0" + (now.getMinutes() + 1)).slice(-2);
        var time = inputDate.get
        var today = (month)+(day);//+(hour)+(minute);
        let options = {
        "separator": ",",
        "newline": "\n",
        "quoteFields": false,
        "excludeColumns": "",
        "excludeRows": "",
        "trimContent": true,
        "filename": today + "出貨葡萄訂單.csv",
        "appendTo": "#output"
        }
        $('table#OrderTable').show();
        showFixContentColumns()
        $("table#OrderTable").table2csv(options); // default action is 'download'
        hideFixContentColumns()
        $('table#OrderTable').hide();

        // Mark orders as exported
        var rawDate = $('#GoogleSpreadShippingDate-input > input').val();
        if (rawDate) {
            var d = new Date(rawDate);
            var shippingDate = d.getFullYear() + "/" + (d.getMonth() + 1) + "/" + d.getDate();
            $.ajax({
                url: "api_markExported",
                type: "post",
                contentType: "application/json",
                data: JSON.stringify({ shippingDate: shippingDate }),
                dataType: "json",
                success: function(data) {
                    if (data.isSuccess) {
                        $("#totoalNumbers").append("<br><span style='color:green'>✓ " + data.msg + "</span>");
                    }
                }
            });
        }
    });

    $( "#exportPNG" ).on( "click", function() {
        var captureArea = document.getElementById('pngCaptureArea');
        if (!captureArea || $.trim($("#totoalNumbers").text()) === '') {
            alert('請先選擇日期查詢出貨資料');
            return;
        }
        var rawDate = $.trim($('#GoogleSpreadShippingDate-input > input').val());
        var inputDate = new Date(rawDate);
        var filename;
        if (rawDate && !isNaN(inputDate.getTime())) {
            var month = ("0" + (inputDate.getMonth() + 1)).slice(-2);
            var day = ("0" + inputDate.getDate()).slice(-2);
            filename = month + day + "出貨總整理.png";
        } else {
            filename = "出貨總整理.png";
        }
        html2canvas(captureArea, { backgroundColor: '#ffffff', scale: 2 }).then(function(canvas) {
            var link = document.createElement('a');
            link.download = filename;
            link.href = canvas.toDataURL('image/png');
            link.click();
        });
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
                   var windowReference = window.open();
                       windowReference.location = data.data;
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

   function queryGoogleSpreadData(){
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
                            $("#totoalNumbers").html(data.totoalNumbers)
                            //$("#totoalNumbersOf2").html(data.totoalNumbersOf2)
                            //$("#totoalNumbersOfPack").html(data.totoalNumbersOfPack)
                            buildDisplayTable()
                       }else{
                           alert("error");
                       }

                    }
                    ,
                    error:function(e){
                            alert("error", e);
                    }
            })

       };

     $( "#GoogleSpreadShippingDate-input > input" ).change(  function(){
        queryGoogleSpreadData()
     });

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
                    if (data.deliveryType == "2"){
                        document.getElementById("deliverySelfPickup-input").checked = true;
                    } else {
                        document.getElementById("deliveryHomeDelivery-input").checked = true;
                    }

                    // show parse method
                    var method = data.parseMethod == "ai" ? "🤖 AI" : "📝 Regex";
                    var info = "解析方式：" + method;
                    if (data.aiError) info += " (" + data.aiError + ")";
                    $("#lblAddDataResponse").text(info)
            },
            error:function(e){
                    alert("error", e);
            }
        })});

// Image upload → AI parse
$( "#imageUpload" ).on( "change", function(){
    var file = this.files[0];
    if (!file) return;
    var formData = new FormData();
    formData.append('image', file);
    $("#imageStatus").text("解析中...");
    $.ajax({
        url: "api_parseImage",
        type: "post",
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false,
        success: function(data){
            $("#imageStatus").text("解析完成");
            if (data.name != "") $("#name-input").val(data.name);
            if (data.address != "") $("#address-input").val(data.address);
            if (data.phone != "") $("#phone-input").val(data.phone);
            if (data.mPhone != "") $("#mPhone-input").val(data.mPhone);
            if (data.numbers != "" && data.numbers != "0") $("#numbers-input").val(data.numbers);
            if (data.arrivalDate != ""){
                var from = data.arrivalDate.split("/");
                var f = new Date(from[0], from[1]-1, parseInt(from[2]));
                var day = ("0" + f.getDate()).slice(-2);
                var month = ("0" + (f.getMonth() + 1)).slice(-2);
                var tomorrow = f.getFullYear()+"-"+(month)+"-"+(day);
                $('#arrivalDate-input').val(tomorrow);
            }
            if (data.arrivalTime == "2"){
                document.getElementById("arriveOnAfternoon-input").checked = true;
            } else if (data.arrivalTime == "1"){
                document.getElementById("arriveTimeOnMorning-input").checked = true;
            }
            if (data.paymentMethod == "2"){
                document.getElementById("cashOnDelivery-input").checked = true;
            } else if (data.paymentMethod == "1"){
                document.getElementById("transfer-input").checked = true;
            }
            $("#lblAddDataResponse").text("");
            // reset file input
            $("#imageUpload").val("");
        },
        error: function(e){
            $("#imageStatus").text("解析失敗");
            $("#imageUpload").val("");
        }
    });
});

$( "#btnAddNewOrder" ).on( "click", function(){
        var isSelfPickup = $("input[name='deliveryType-input']:checked").val() == "自取";

        if (!isSelfPickup) {
            if($("#name-input").val() == "" ){
                alert("請輸入姓名")
                return
            }
            if($("#address-input").val() == "" ){
                alert("請輸入地址")
                return
            }
            if($("#phone-input").val() == "" && $("#mPhone-input").val() == ""){
                alert("請輸入電話")
                return
            }
        }
        if($("#numbers-input").val() == "" || $("#numbers-input").val() == "0"){
            alert("請輸入數量")
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
                   $("#numbers-input").val("4")
                   $("#userComment-input").val("")
                   // clear input textarea
                   $("#orderForm > div > div:nth-child(1) > textarea").val("")
                   radiobtn = document.getElementById("arriveTimeOnMorning-input");
                   radiobtn.checked = true;
                   radiobtn = document.getElementById("transfer-input");
                   radiobtn.checked = true;
                   document.getElementById("deliveryHomeDelivery-input").checked = true;
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
            $('#GoogleSpreadShippingDate-input').val(tomorrow);
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