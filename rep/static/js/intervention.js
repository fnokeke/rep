
var intervention = (function() {

  /////////////////////////////
  // upload images and texts
  /////////////////////////////
  $('#btn-open-upload-modal').click(function() {
    console.log('upload modal clicked.');
    $('#upload-image-modal').modal('show');
  });

  $('#upload-btn').click(function(event) {
    var image,
      text,
      response_field,
      form_data;
    event.preventDefault();

    image = $('#uploaded-image').get(0).files[0];
    text = $('#uploaded-text').val();
    if (!text) {
      text = "";
    }
    response_field = '#upload-status';

    if (!image && !text) {
      show_error_msg(response_field, 'You need to add either an image and/or a text.');
      return;
    }

    form_data = new FormData();

    if (image) {
      form_data.append('image', image);
      form_data.append('image_name', image.name);
    }

    if (text) {
      form_data.append('text', text);
    }

    var code = $('#code_from_hidden_element').val();
    form_data.append('code', code);

    console.log('text going:', text);

    $.ajax({
      url: '/upload/intervention',
      success: function(resp) {
        show_success_msg(response_field, 'Successfully uploaded: ' + resp);
      },
      error: function(e) {
        show_error_msg(response_field, 'Upload error. Pls contact researcher. ' + e.statusText);
      },
      complete: function(e) {
        setTimeout(function() {
          show_plain_msg(response_field, '');
          $('#upload-image-modal').modal('hide');
          $('#uploaded-image').val('');
          $('#uploaded-text').val('');
          window.location.href = window.location.href;
        }, 1500);
      },
      data: form_data,
      type: 'POST',
      cache: false,
      contentType: false,
      processData: false
    });
    return false;

  });

  $('#reset-table-btn').click(function() {
    $('#intv-table-view').html('');
    update_intv_table();
  });

  $('#save-group-btn').click(function() {

    var experiment_code = $('#code_from_hidden_element').val();
    var no_of_condition = parseInt($('#no-of-condition').val());
    var ps_per_condition = $('#ps-per-condition').val();

    var response_field = '#group-status';
    var url = '/update/group';
    var data = {
      'code': experiment_code,
      'no_of_condition': no_of_condition,
      'ps_per_condition': ps_per_condition
    };

    $.post(url, data).done(function(resp) {
      show_success_msg(response_field, 'Group info successfully updated. Refreshing...<br/>');
      setTimeout(function() {
        window.location.href = window.location.origin + window.location.pathname;
      }, 1000);
    }).fail(function(error) {
      show_error_msg(response_field, 'Error saving: ' + error.statusText);
    });

  });

  $('#save-table-btn').click(function() {
    var intv_notif = $('#intv-notif').find(":selected").val();
    var intv_every = $('#intv-every').val();
    var intv_repeat = $('#intv-repeat').val();
    var intv_when = $('#intv-when').val();
    var user_window_enabled = $('#user-window-enabled').val() === "True";
    var experiment_code = $('#code_from_hidden_element').val();
    var user_window_hours = $('#user-window-hours').val();
    var free_hours_before_sleep = $('#free-hours-before-sleep').val();

    // disable alarm time if user window is enabled
    if (user_window_enabled) {
      intv_when = '';
      user_window_hours = parseInt(user_window_hours);
      free_hours_before_sleep = parseInt(free_hours_before_sleep);
    } else {
      user_window_hours = -1;
      free_hours_before_sleep = -1;
    }

    var factor = intv_every === 'Daily' ? 1 : 7;
    var no_of_days = intv_repeat * factor;

    var intv_start_date = $('#intv-start-date').val();
    var intv_start_datetime = to_daylight_dt(intv_start_date);

    var intv_end_datetime = to_daylight_dt(intv_start_date);
    intv_end_datetime.setDate(intv_end_datetime.getDate() + no_of_days);

    var end_exp = $('#edit-end-date').val();
    var experiment_end_datetime = to_daylight_dt(end_exp);

    var response_field = '#intv-table-status';
    if (intv_end_datetime.getTime() > experiment_end_datetime.getTime()) {
      show_error_msg(response_field, 'Intervention is beyond experiment end date.');
      return;
    }

    var intv_type = $('#intv-type').val();
    var no_of_condition = parseInt($('#no-of-condition').val());
    var treatment = intv_type == "text_image" ? extract_treatment(no_of_condition) : "";

    var url = '/add/intervention';
    var data = {
      'condition': no_of_condition,
      'treatment': treatment,
      'intv_type': intv_type,
      'user_window_hours': user_window_hours,
      'free_hours_before_sleep': free_hours_before_sleep,
      'notif_id': intv_notif,
      'code': experiment_code,
      'start': intv_start_datetime.getTime(), // UTC
      'end': intv_end_datetime.getTime(), // UTC
      'every': intv_every,
      'when': intv_when,
      'repeat': intv_repeat
    };


    $.post(url, data).done(function(resp) {
      show_success_msg(response_field, 'Intervention successfully saved.<br/>');
      console.log('success intv resp: ', resp);
      window.location.href = window.location.origin + window.location.pathname;
    }).fail(function(error) {
      show_error_msg(response_field, 'Error saving intervention: ' + error.statusText);
      console.log('intv save error:', error);
    });
  });

  function to_daylight_dt(datestr) {
    var tmp = new Date();
    var arr = datestr.split("-");

    tmp.setYear(parseInt(arr[0]));
    tmp.setMonth(parseInt(arr[1]) - 1);
    tmp.setDate(parseInt(arr[2]));
    tmp.setHours(0);
    tmp.setMinutes(0);
    tmp.setSeconds(0);
    tmp.setMilliseconds(0);

    return tmp;
  }

  function extract_treatment(no_of_condition) {
    var all_treat = {};
    var treat;
    var treat_id;

    for (var i = 0; i < no_of_condition; i++) {
      treat_id = '#intv-text-image-' + i;
      treat = $(treat_id).find(":selected").val();
      all_treat['group' + (i + 1)] = treat;
    }

    return JSON.stringify(all_treat);
  }

  /////////////////////////////
  /// delete archived intv ////
  /////////////////////////////

  function delete_intv(intv) {
    var prompt = "Are you sure you want to delete permanently?\nIntervention created at: {0}".format(intv.created_at);
    if (confirm(prompt) === false) {
      return;
    }

    var response_field = '#delete-intv-status';
    var url = '/delete/intervention';
    var data = {
      'created_at': intv.created_at
    };

    $.post(url, data).done(function(resp) {
      show_success_msg(response_field, resp);
      window.location.href = window.location.origin + window.location.pathname;
    }).fail(function(error) {
      show_error_msg(response_field, error.statusText);
    });
  }

  var exposed = {
    'delete_intv': delete_intv
  };

  return exposed;

})();
