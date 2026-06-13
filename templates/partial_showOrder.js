<script>
<!--    var calenderPickableDates = {{orderDates|tojson}}-->
    var enableDatesArray = {{orderDates|tojson}};
    var sortDatesArry = [];
           var minDt = new Date(enableDatesArray[0]);
           var maxDt = new Date(enableDatesArray[enableDatesArray["length"]-1]);
           $('#GoogleSpreadShippingDate-input').datepicker({
                  format: "yyyy/mm/dd (DD)",
                  autoclose: true,
                  startDate: minDt,
                  endDate: maxDt,
                  todayHighlight: true,
                  language: "zh-TW",

                  beforeShowDay: function (date) {
                     var dt_ddmmyyyy = date.getFullYear() + '/' + (date.getMonth() + 1) + '/' + date.getDate() ;
                     return (enableDatesArray.indexOf(dt_ddmmyyyy) != -1);
                  }
              });

    // Auto-load tomorrow's orders on page load if data exists
    var _tomorrow = new Date();
    _tomorrow.setDate(_tomorrow.getDate() + 1);
    var _tomorrowKey = _tomorrow.getFullYear() + '/' + (_tomorrow.getMonth() + 1) + '/' + _tomorrow.getDate();
    if (enableDatesArray.indexOf(_tomorrowKey) !== -1) {
        $('#GoogleSpreadShippingDate-input').datepicker('setDate', _tomorrow);
        $('#GoogleSpreadShippingDate-input > input').trigger('change');
    }

</script>