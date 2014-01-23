function isTimeRangeAvailable(timeRange, apt_time) {
  for (i = 0; i < apt_time.length; i++) {
    if ((apt_time[i][0] > timeRange[0] && apt_time[i][0] < timeRange[1]) ||
        (apt_time[i][1] > timeRange[0] && apt_time[i][1] < timeRange[1]))
      return false;
  }

  return true;
}

function slideTime(event, ui){
  var val0 = ui.values[0],
	  val1 = ui.values[1],
	  minutes0 = parseInt(val0 % 60, 10),
	  hours0 = parseInt(val0 / 60 % 24, 10),
	  minutes1 = parseInt(val1 % 60, 10),
	  hours1 = parseInt(val1 / 60 % 24, 10);

  var startTime = formatTime(hours0, minutes0);
  var endTime = formatTime(hours1, minutes1);
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

  if(isTimeRangeAvailable([val0, val1], $(this).slider("option", "apt_time"))){
    $("#time-notify").hide();
    $("input[type=submit]").removeAttr("disabled");
  }
  else {
    $("#time-notify").text('Sorry but your selection contains unavailable time range').css({color:'#b94a48'});
    $("input[type=submit]").attr("disabled", "disabled");
    $("#time-notify").show();
  }
}

function createTime(event, ui) {
  var values = $(this).slider("option", "values"),
      val0 = values[0],
	  val1 = values[1],
	  minutes0 = parseInt(val0 % 60, 10),
	  hours0 = parseInt(val0 / 60 % 24, 10),
	  minutes1 = parseInt(val1 % 60, 10),
	  hours1 = parseInt(val1 / 60 % 24, 10);

  var startTime = formatTime(hours0, minutes0);
  var endTime = formatTime(hours1, minutes1);
  $("#start_time").val(val0);
  $("#end_time").val(val1);
  $("#time").text(startTime + ' - ' + endTime);
}

function renderAvailableBar(apt_time, bar_length) {
  if (apt_time.length == 0) {
	$("<div class=\"bar bar"+i+"\"></div>").appendTo("#time-slider");
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

function time_slider_init_or_reload () {
  $.getJSON('/appointment/',
            {'timezone': $("#timezone").val(), 'date': $("#date").val()},
            function(data) {
    var minutes_a_day = 1440;
    var apt_time = data.apt_time_slider;
    $("#slider-range").slider({
      range: true,
      min: 0,
      max: minutes_a_day,
      apt_time: apt_time,
      values: [0, 0],
      step: 15,
      slide: slideTime,
      create: createTime
    });
    renderAvailableBar(apt_time, minutes_a_day);
  });
}

function timezone_init() {
  var offset = new Date().getTimezoneOffset();
  $("#timezone").val((-offset/60).toFixed(2))

  $("#timezone").change(function() {
    time_slider_init_or_reload();
  });

  $("#date").change(function() {
    time_slider_init_or_reload();
  });
}

timezone_init()
time_slider_init_or_reload()
