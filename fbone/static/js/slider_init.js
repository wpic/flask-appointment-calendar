function isTimeRangeOK(timeRange, apt_time) {
  if (timeRange[0] == timeRange[1])
    return false;
  for (i = 0; i < apt_time.length; i++) {
    if ((apt_time[i][0] == 0 && apt_time[i][1] == 0) ||
        (apt_time[i][0] == 1440 && apt_time[i][1] == 1440))
      continue;
    if ((timeRange[0] > apt_time[i][0] && timeRange[0] < apt_time[i][1]) ||
        (timeRange[1] > apt_time[i][0] && timeRange[1] < apt_time[i][1]) ||
        (timeRange[0] <= apt_time[i][0] && timeRange[1] >= apt_time[i][1]))
      return false;
  }

  return true;
}

function slideTime(event, ui) {
  var apt_time = $(this).slider("option", "apt_time");
  reloadTimeRangeSlider(ui.values, apt_time, event, ui);
}

function createTime(event, ui) {
  var apt_time = $(this).slider("option", "apt_time");
  var timeRange= $(this).slider("option", "values");
  reloadTimeRangeSlider(timeRange, apt_time, event, ui);
}

function reloadTimeRangeSlider(timeRange, apt_time, event, ui) {
  var val0 = timeRange[0],
      val1 = timeRange[1],
	  minutes0 = parseInt(val0 % 60, 10),
	  hours0 = parseInt(val0 / 60 % 25, 10), // show 24:00 when val0 == 1440
	  minutes1 = parseInt(val1 % 60, 10),
	  hours1 = parseInt(val1 / 60 % 25, 10); // show 24:00 when val1 == 1440

  var startTime = formatTime(hours0, minutes0);
  var endTime = formatTime(hours1, minutes1);
  var message;
  // console.log("val0: " + val0 + "\n" +
  //             "val1: " + val1 + "\n" +
  //             "hours0: " + hours0 + "\n" +
  //             "minute0: " + minutes0 + "\n" +
  //             "hours1: " + hours1 + "\n" +
  //             "minutes1: " + minutes1 + "\n" +
  //             "startTime: " + startTime + "\n" +
  //             "endTime: " + endTime)
  $("#start_time").val(val0);
  $("#end_time").val(val1);
  $("#time").text(startTime + ' - ' + endTime);

  if(isTimeRangeOK([val0, val1], apt_time)) {
    $("#time-notify").hide();
    $("input[type=submit]").removeAttr("disabled");
  }
  else {
    if (val0 == val1)
      message = "Start time and end time is the same.";
    else
      message = "Your selection contains occupied time range";
    $("#time-notify").text(message).css({color: '#B94A48'});
    $("input[type=submit]").attr("disabled", "disabled");
    $("#time-notify").show();
  }
}

function renderAvailableBar(apt_time, bar_length) {
  $('.time-picker div[class^="bar"]').remove()
  if (apt_time.length == 0) {
    return;
  }

  for(i = 0; i < apt_time.length; i++){
	$("<div class=\"bar bar"+i+"\"></div>").appendTo("#time-slider");
	$(".bar"+i).css({left: (apt_time[i][0] * 100.0)/bar_length + "%",
                     right:(bar_length - apt_time[i][1]) * 100.0/bar_length+"%"})
  }
}

function formatTime(hours, minutes) {
  var time;
  minutes = minutes + "";
  if (minutes.length == 1) {
	minutes = "0" + minutes;
  }
  return hours + ":" + minutes;
}

function time_slider_init_or_reload (timeRange) {
  $.getJSON('/appointment/',
            {'timezone': $("#timezone").val(),
             'date': $("#date").val()},
            function(data) {
    var minutes_a_day = 1440;
    var apt_time = data.apt_time_slider_minutes;
    $("#slider-range").slider({
      range: true,
      min: 0,
      max: minutes_a_day,
      apt_time: apt_time,
      values: timeRange,
      step: 15,
      slide: slideTime,
      create: createTime
    });

    reloadTimeRangeSlider(timeRange, apt_time, null, null);
    renderAvailableBar(apt_time, minutes_a_day);
  });
}

function timezone_init() {
  var offset = new Date().getTimezoneOffset();
  $("#timezone").val((-offset/60).toFixed(2))

  $("#timezone").change(function() {
    var timeRange = $('#slider-range').slider("values");
    time_slider_init_or_reload(timeRange);
  });

  $('.datetimepicker-no-time').on('changeDate', function(e) {
    var timeRange = $('#slider-range').slider("values");
    time_slider_init_or_reload(timeRange);
  });
}

timezone_init()
time_slider_init_or_reload([480, 600])
