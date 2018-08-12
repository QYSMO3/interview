var dialog_newTime, form,
name = $( "#name" ),
tips = $( ".validateTips" );

function updateTips( t ) {
  tips
    .text( t )
    .addClass( "ui-state-highlight" );
  setTimeout(function() {
    tips.removeClass( "ui-state-highlight", 1500 );
  }, 500 );
}

function addTime() {
  var valid = true;
  if ( valid ) {
  	$.ajax({
	    url: '/availables/',
	    type: 'POST',
	    dataType: 'json',
		traditional: true,
	    data: {
	        'userID':$('#h_id')[0].innerHTML,
	        'date':$('#input_date').val(),
	        'start':$('#start_from').val(),
	        'end':$('#end_to').val()
	    },
	    success: function(){
	    	alert('success!')
	    	location.reload()
	    },
	    error: function(){
	        alert('failed')
	    }
	})
    dialog_newTime.dialog( "close" );
  }
  return valid;
}

dialog_newTime = $('#dialog-newTime').dialog({
  autoOpen: false,
  height: 400,
  width: 350,
  modal: true,
  buttons: {
    "save": addTime,
    Cancel: function() {
      dialog_newTime.dialog( "close" );
    }
  },
  	close: function() {
    form[ 0 ].reset();
  }
});

form = dialog_newTime.find( "form" ).on( "submit", function( event ) {
  event.preventDefault();
  addTime();
});

$("#new_time" ).button().on( "click", function() {
  dialog_newTime.dialog("open");
});

$("#form_date").datetimepicker({
        format: "yyyy-mm-dd ",
        minView: "month",
        autoclose: true,
        todayBtn: true,
        pickerPosition: "bottom-left"
    });