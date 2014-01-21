function isAvailableTimeRange(timeRange, available) {
  for (i = 0; i < available.length - 1; i++) {
    if ((timeRange[0] >= available[i] && timeRange[1] <= available[i + 1]) &&
        (timeRange[1] >= available[i] && timeRange[1] <= available[i + 1])) {
      if (i % 2 == 0)
        return true;
    }
  }

  return false;
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
  $("#time").text(startTime + ' - ' + endTime);

  if(isAvailableTimeRange([val0, val1], $(this).slider("option", "available"))){
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
  $("#time").text(startTime + ' - ' + endTime);
}

function renderAvailableBar(available, bar_length){
  for(i = 0; i < available.length; i += 2){
	$("<div class=\"bar bar"+i+"\"></div>").appendTo("#time-slider");
	$(".bar"+i).css({left: (available[i] * 100.0)/bar_length + "%",
                     right:(bar_length - available[i+1]) * 100.0/bar_length+"%"})
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

function time_slider_init_or_reload (available) {
  var minutes_a_day = 1439;

  $("#slider-range").slider({
    range: true,
    min: 0,
    max: minutes_a_day,
    values: [available[0], available[1]],
    available: available,
    step: 15,
    slide: slideTime,
    create: createTime
  });

  renderAvailableBar(available, minutes_a_day);
}

time_slider_init_or_reload([150, 300, 600, 900, 1200, 1320]);
