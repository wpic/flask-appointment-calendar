(function($) {

  "use strict";

  var options = {
    events_source: [
      {
        "id": 293,
        "title": "Event 1",
        "url": "http://example.com",
        "class": 'event-important',
        "start": 12039485678000, // Milliseconds
        "end": 1234576967000 // Milliseconds
      }
    ],
    view: 'month',
    tmpl_path: 'static/tmpls/',
    tmpl_cache: false,
    holidays: {},
    onAfterEventsLoad: function(events) {
      if(!events) {
        return;
      }
      var list = $('#eventlist');
      list.html('');

      $.each(events, function(key, val) {
        $(document.createElement('li'))
        .html('<a href="' + val.url + '">' + val.title + '</a>')
        .appendTo(list);
      });
    },
    onAfterViewLoad: function(view) {
      $('.page-header h3').text(this.getTitle());
      $('.btn-group button').removeClass('active');
      $('button[data-calendar-view="' + view + '"]').addClass('active');

      // disable "week" popup in month view.
      $('.cal-month-box .cal-row-fluid').off('mouseenter').off('mouseleave');

      // redirect to appointment page when click on a date
      $('.cal-month-box *[data-cal-date]').off('click');
      $('.cal-month-box *[data-cal-date]').each(function() {
        var today = new Date();
        today.setHours(0, 0, 0, 0);
        var calDate = new Date($(this).data('calDate'))
        if (calDate >= today)
          $(this).click(function () {
            window.location.href = "/appointment/create?date=" + $(this).data('calDate');
          })
        else
          $(this).css({cursor: "default"})
      });

      // disable double click events in cal-cell of month view
      $('.cal-month-box .cal-cell1').off('dblclick');
      // delegate click event to its children
      $('.cal-month-box .cal-cell1').click(function() {
        this.children[0].children[0].click();
        return false;
      })

      // disable original click events on cal-cell of year view
      $('.cal-year-box .cal-cell').off('dblclick').off('click');
      // delegate click event to its children
      $('.cal-year-box .cal-cell').click(function() {
        this.children[0].click();
        return false;
      })
    },
    classes: {
      months: {
        general: 'label'
      }
    }
  };

  var calendar = $('#calendar').calendar(options);

  $('.btn-group button[data-calendar-nav]').each(function() {
    var $this = $(this);
    $this.click(function() {
      calendar.navigate($this.data('calendar-nav'));
    });
  });

  $('.btn-group button[data-calendar-view]').each(function() {
    var $this = $(this);
    $this.click(function() {
      calendar.view($this.data('calendar-view'));
    });
  });

  $('#first_day').change(function(){
    var value = $(this).val();
    value = value.length ? parseInt(value) : null;
    calendar.setOptions({first_day: value});
    calendar.view();
  });

  $('#language').change(function(){
    calendar.setLanguage($(this).val());
    calendar.view();
  });

  $('#events-in-modal').change(function(){
    var val = $(this).is(':checked') ? $(this).val() : null;
    calendar.setOptions({modal: val});
  });
  $('#events-modal .modal-header, #events-modal .modal-footer').click(function(e){
    //e.preventDefault();
    //e.stopPropagation();
  });
}(jQuery));
