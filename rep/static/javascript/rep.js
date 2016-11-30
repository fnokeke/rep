//
// rep.js
//

$(document).ready(function() {

  // enable string formatting: '{0}{1}'.format(var1, var2)
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/\{(\d+)\}/g, function(m, n) {
      return args[n];
    });
  };

  // fetch param from url: xyz.com?enable=yes ---> urlParam(enable) returns yes
  $.url_param = function(name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results === null) {
      return null;
    } else {
      return results[1] || 0;
    }
  };

  var errors = {
    'internal_server_error': 'oops, cannot complete request at this time. contact admin.',
    'method_not_allowed': 'profile update failed. try again later or contact admin.'
  };

  // #################################################
  // helper functions
  // #################################################
  function disable(btn_id) {
    $(btn_id).prop("disabled", true);
  }

  function enable(btn_id) {
    $(btn_id).prop("disabled", false);
  }

  function show_busy_div(div) {
    $(div).html('Processing...').css('color', 'orange');
  }

  function show_success_msg(div, msg) {
    $(div).html(msg).css('color', 'green');
  }

  function show_plain_msg(div, msg) {
    $(div).html(msg).css('color', 'black');
  }

  function show_error_msg(div, msg) {
    $(div).html(msg).css('color', 'red');
  }


  function submit_checkbox_val(field, input) {
    var url = 'settings/tracking/' + field + '/' + input;
    var response_field = '#' + field + '-checkbox-status';

    $.get(url, function(resp) {
      // show_success_msg(response_field, resp);
      var results = JSON.parse(resp);
      console.log('results: ', results);
    }).fail(function(error) {
      show_error_msg(response_field, errors.internal_server_error);
    });
  }


  // #################################################
  // authenticate/connect data streams
  // #################################################
  $('#signin-btn').click(function() {
    window.location.href = '/google_login';
  });

  $('#mturk-auth-moves-btn').click(function() {

    if ($('#mturk-worker-id').val() === '') {
      show_error_msg('#mturk-submit-status', 'Submit a valid worker id before you connect Moves app.');
      return;
    }
    window.location.href = '/mturk-auth-moves';
  });

  $('#auth-moves-btn').click(function() {
    $('#auth-status-div').html('connecting to moves...');
    window.location.href = '/auth-moves';
  });

  $('#auth-pam-btn').click(function() {
    window.location.href = '/auth-pam';
  });

  $('#auth-rt-btn').click(function() {
    window.location.href = '/auth-rt';
  });


  // #################################################
  // checkboxes for activating datastreams
  // #################################################
  $('#location-checkbox-btn').on('change', function() {
    submit_checkbox_val('location', this.checked);
  });

  $('#mood-checkbox-btn').on('change', function() {
    submit_checkbox_val('mood', this.checked);
  });

  $('#sn-checkbox-btn').on('change', function() {
    submit_checkbox_val('sn', this.checked);
  });


  // #################################################
  // dropdowns
  // #################################################

  $('#dropdown-action li').on('click', function() {
    var selected = $(this).text();
    $('#dropdown-action-label').html(selected);
  });

  $('#dropdown-calendar li').on('click', function() {
    var selected = $(this).text();
    $('#dropdown-cal-label').html(selected);
  });

  $('#dropdown-cmd li').on('click', function() {
    var selected = $(this).text();
    $('#dropdown-cmd-label').html(selected);
  });

  $('#execute-config-btn').click(function() {
    var calendar_selected = $('#dropdown-cal-label').text().replace(/\s/g, ''); // regex removes all spaces in string
    var command_selected = $('#dropdown-cmd-label').text().replace(/\s/g, ''); // regex removes all spaces in string
    var response_field = '#execute-config-status';

    // if (calendar_selected === 'ChooseDatastream' || command_selected === 'ChoooseCommand') {
    if (calendar_selected.indexOf('Choose') >= 0 || command_selected.indexOf('ChoooseCommand') >= 0) {
      show_error_msg(response_field, 'Both entries must be selected from dropdown menu.');
      return;
    }

    var url = '/settings/execute/' + calendar_selected + '/' + command_selected;
    show_busy_div(response_field);

    $.get(url, function(resp) {
      show_success_msg(response_field, resp);
    }).fail(function(error) {
      show_error_msg(response_field, errors.internal_server_error);
    });
  });

  // #################################################
  // other buttons

  var gen_code = $.url_param('gen_code');
  if (gen_code) {
    localStorage.gen_code = gen_code;
  }
  var gen_txt = localStorage.gen_code ?
    '<strong>' + localStorage.gen_code + '</strong>' :
    '(<em>no code yet<em/>).';
  $('#gen-code-id').html(gen_txt);
  $('#mturk-worker-id').val(localStorage.worker_id);

  $('#mturk-submit-btn').click(function(event) {
    event.preventDefault();

    var worker_id = $('#mturk-worker-id').val();
    worker_id = worker_id.replace(/[^a-z0-9\s]/gi, '');
    var response_field = '#mturk-submit-status';

    if (worker_id === '') {
      show_error_msg(response_field, 'Please submit a valid worker id.');
      return;
    }

    var url = '/mturk/worker_id';
    var data = {
      'worker_id': worker_id
    };

    $.post(url, data).done(function(resp) {
      localStorage.worker_id = worker_id;
      show_success_msg(response_field, 'Successfully submitted worker id.');
    }).fail(function(error) {
      var msg = 'Submission error. Pls contact MTurk Requester (Error: {0} / {1}).'.format(error.status,
        error.statusText);
      show_error_msg(response_field, msg);
    });

  });


  $('#send-img-btn').click(function(event) {
    event.preventDefault();
    var response_field = '#upload-status';
    var image = $('#image').get(0).files[0];
    if (!image) {
      show_error_msg(response_field, 'select an image then click upload.');
      return;
    }
    var formData = new FormData();
    formData.append('image', image);
    formData.append('image_name', image.name);

    $.ajax({
      url: '/upload/image',
      success: function(e) {
        console.log('resp: ', e);
        show_success_msg(response_field, 'Image successfully uploaded.');
        $('#fetch-all-imgs-btn').click();
      },
      error: function(e) {
        show_error_msg(response_field, 'Image upload error. Pls contact admin.');
      },
      complete: function(e) {
        setTimeout(function() {
          $('#upload-image-modal').modal('hide');
          show_plain_msg(response_field, '');
          $('#image').val('');
        }, 500);
      },
      data: formData,
      type: 'POST',
      cache: false,
      contentType: false,
      processData: false
    });
    return false;
  });
  // #################################################

  $('#send-txt-btn').click(function(event) {
    event.preventDefault();
    var response_field = '#txt-status';
    var txt = $('#txt').val();
    if (!txt) {
      show_error_msg(response_field, 'Cannot submit empty text');
      return;
    }

    var url = '/upload/txt';
    var data = {
      'txt': txt
    };

    $.post(url, data).done(function(resp) {
      show_success_msg(response_field, 'Message successfully sent.');
    }).fail(function(error) {
      show_error_msg(response_field, 'Message upload error. Pls contact admin.');
    }).always(function(e) {
      setTimeout(function() {
        $('#upload-image-modal').modal('hide');
        show_plain_msg(response_field, '');
        $('#txt').val('');
      }, 500);
    });

  });

  $('#fetch-all-imgs-btn').click(function(event) {
    event.preventDefault();

    var response_field = '#stored-img-div';
    var url = '/fetch/images';
    $.get(url, function(resp) {
      var results = JSON.parse(resp);
      var summary =
        '<table class = "table table-striped table-bordered"> <tr> <th class="col-md-2">Intervention Day</th> <th class="">Image</th> <th class="">Text</th><th class="col-md-1">Edit/Delete</th> </tr>';
      var row;

      var texts = [
        '50 lines of code per day amounts to one library per month',
        'In 5 minutes, you could set up a server on AWS.',
        'How much of your work goals have been met this week?',
        'When next will you update your adviser about your work accomplished'
      ];
      for (var i = 0; i < results.length; i++) {
        row =
          '<tr> <td>{0}</td> <td><img src="{1}" alt="Image {0}" class="img-thumbnail col-img"></td> <td>{2}</td> <td> <button type="button" class="btn btn-sm btn-primary"' +
          'data-toggle="modal" data-target="#delete-image-modal"> <span class="glyphicon glyphicon-pencil"></span> </button> ' +
          '<button type="button" class="btn btn-sm btn-danger" data-toggle="modal" data-target="#delete-image-modal">' +
          '<span class="glyphicon glyphicon-trash"></span> </button> </td> </tr>';
        row = row.format(i + 1, results[i], texts[i % texts.length]);
        summary += row;
      }

      summary += '</table>';

      show_plain_msg(response_field, summary);
    }).fail(function(error) {
      show_error_msg(response_field, 'Error fetching all images. Contact Admin.');
    });

  });

  $('#fetch-all-imgs-btn').hide();
  $('#fetch-all-imgs-btn').click(); // show images by default

  $('#perform-analysis-btn').click(function() {
    var datapoint = $('#dropdown-action-label').text().replace(/\s/g, '').toLowerCase(); // regex removes all spaces in string
    var response_field = '#analysis-status';
    var dates = $('#experiment-dates').val();
    dates = dates.replace(/\s/g, '').split(',');
    if (dates.length < 2) {
      show_error_msg(response_field, 'You need to select 4 dates in order to perform analysis.');
      return;
    }

    // study_begin, intervention_begin, intervention_end, study_end);
    var url = 'researcher_analysis/{0}/{1}/{2}/{3}/{4}'.format(datapoint, dates[3], dates[2], dates[1], dates[0]);
    $.get(url, function(resp) {
      var summary, results, uid, counter;

      summary = '<strong> stats for {0} </strong>'.format(datapoint);
      summary += '<table class="table table-striped">' +
        '<tr><th> User </th> <th> Baseline </th> <th> Interventions </th> <th> Follow Up </th> </tr>';

      counter = 0;
      results = JSON.parse(resp);

      for (var row in results) {
        uid = 'user {0}'.format(counter);
        counter++;

        info = results[row];
        summary += '<tr> <td>{0}</td> <td>{1}</td> <td>{2}</td> <td>{3}</td> </tr>'.format(uid, info.baseline,
          info.intervention, info.follow_up);
      }
      summary += '</table>';
      show_plain_msg(response_field, summary);

    }).fail(function(error) {
      show_error_msg(response_field, errors.internal_server_error);
    });

  });

  // reset all previous entries
  $('#reset-btn').click(function() {

    var r = confirm(
      "Are you sure about resetting calendar? Everything will be wiped out."
    );
    if (r) {
      $('#cal-status-div').html('Resetting calendar...');
      $.get('/settings/reset', function(resp) {
        $('#cal-status-div').html(resp);
      });
    } else {
      $('#cal-status-div').html('');
    }
  });

  $('#change-btn').click(function() {
    var r = confirm(
      "Are you sure about changing calendar? Current data will be discarded."
    );
    if (r) {
      $('#cal-status-div').html('Changing calendar...');
      $.get('/settings/change', function(resp) {
        $('#cal-status-div').html(resp);
        window.location.href = '/auth-gcal';
      });
    } else {
      $('#cal-status-div').html('');
    }
  });

  // delete location calendar
  $('#delete-btn').click(function() {
    var r = confirm(
      "Are you sure you want to completely remove calendar?");
    if (r) {
      $('#cal-status-div').html('deleting SLM-Location calendar...');
      $.get('/settings/delete', function(resp) {
        $('#cal-status-div').html(resp);
      });
    } else {
      $('#cal-status-div').html('');
    }
  });

  $('#moves-export-btn').click(function() {

    var response_field = '#moves-status-div';
    var date_str = $('#loc-date').val();
    var yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);

    var request;

    if (date_str === '') {
      date_str = yesterday.toJSON().slice(0, 10);
      $('#loc-date').val(date_str);
    }

    url = '/data-moves/' + date_str;
    $('#moves-status-div').html('Exporting moves data for ' + date_str + '...');

    $.get(url, function(resp) {
      var response_field = '#moves-status-div';

      if (typeof(resp) === 'string') {
        show_success_msg(response_field, resp);
        return;
      }

      var result = JSON.parse(resp);
      result = typeof(result) !== 'object' ? JSON.parse(result) : result;

      if ('error' in result) {
        show_error_msg(response_field, 'Error: ' + result.error);
        return;
      }

      if (result.length < 1) {
        $('#moves-status-div').html();
        show_error_msg(response_field, 'No data available.');
        return;
      }

      show_success_msg('#moves-status-div', resp);

    }).fail(function(error) {
      show_error_msg(response_field, errors.internal_server_error);
    });

  });

  $('#pam-export-btn').click(function() {

    var response_field = '#pam-status-div';
    var date_str = $('#pam-date').val();
    var yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    var request;

    if (date_str === '') {
      date_str = yesterday.toJSON().slice(0, 10);
      $('#pam-date').val(date_str);
    }

    url = '/data-pam/' + date_str;
    $(response_field).html('Exporting PAM data for ' + date_str + '...');

    $.get(url, function(resp) {
      var response_field = '#pam-status-div';

      if (typeof(resp) === 'string') {
        show_success_msg(response_field, resp);
        return;
      }

      var result = JSON.parse(resp);
      console.log('response: ', result);

      if ('error' in result) {
        show_error_msg(response_field, 'Error: ' + result.error);
        return;
      }

      if (result.length < 1) {
        show_error_msg(response_field, 'No data available.');
        return;
      }

      show_success_msg(response_field, resp);

    }).fail(function(error) {
      show_error_msg(response_field, errors.internal_server_error);
    });

  });


  $('#rt-export-btn').click(function() {

    var response_field = '#rt-status-div';
    var date_str = $('#rt-date').val();
    var yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    var request;

    if (date_str === '') {
      date_str = yesterday.toJSON().slice(0, 10);
      $('#rt-date').val(date_str);
    }

    url = '/data-rt/' + date_str;
    $(response_field).html('Exporting RescueTime data for ' + date_str + '...');

    $.get(url, function(resp) {
      var response_field = '#rt-status-div';

      if (typeof(resp) === 'string') {
        show_success_msg(response_field, resp);
        return;
      }

      var result = JSON.parse(resp);
      console.log('result: ', result);

      var printout;
      var tmp = result.row_headers.join(',&#09;&#09;&#09;'); // &#09 is tab
      printout = '<b>' + tmp + '</b><br>';

      result.rows.forEach(function(row) {
        tmp = row.join(',&#09;&#09;&#09;');
        printout += tmp + '<br>';
      });

      if (resp.length < 1) {
        show_error_msg(response_field, 'No data available.');
        return;
      }

      show_success_msg(response_field, printout);

    }).fail(function(error) {
      show_error_msg(response_field, errors.internal_server_error);
    });

  });

  // #################################################
  // update profile fields
  // #################################################
  $('#update-profile-btn').click(function() {
    var firstname = $('#firstname-field').val();
    var lastname = $('#lastname-field').val();
    var gender = $('#gender-field').val();
    var data;
    var url = 'settings/profile/update';

    if (firstname === '' && lastname === '' && gender === '') {
      show_error_msg('#update-profile-status', 'You cannot have all fields empty.');
      return;
    }

    data = {
      'firstname': firstname,
      'lastname': lastname,
      'gender': gender,
    };

    $.post(url, data).done(function(resp) {
      show_success_msg('#update-profile-status', 'profile successfully updated');
    }).fail(function(error) {
      show_error_msg('#update-profile-status', errors.method_not_allowed);
    });

  });

  // #################################################
  // page animation for message
  // #################################################
  $(".alert-dismissible").each(function(index) {
    var $me = $(this);
    $me.delay(2000 + 800 * index).fadeTo(200, 0).slideUp(200,
      function() {
        $me.alert('close');
      });
  });

}); // (document).ready
