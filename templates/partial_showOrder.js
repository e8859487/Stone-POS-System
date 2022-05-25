<script>
<!--    var calenderPickableDates = {{orderDates|tojson}}-->
    var enableDatesArray = {{orderDates|tojson}};
    var sortDatesArry = [];
           var minDt = new Date(enableDatesArray[0]);
           var maxDt = new Date(enableDatesArray[enableDatesArray["length"]-1]);
           $('#GoogleSpreadArrivalDate-input').datepicker({
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

</script>