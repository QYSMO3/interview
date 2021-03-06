$( function() {
	var dialog, form,

	  name = $( "#name" ),
	  allFields = $( [] ).add( name ),
	  tips = $( ".validateTips" );

	function updateTips( t ) {
	  tips
	    .text( t )
	    .addClass( "ui-state-highlight" );
	  setTimeout(function() {
	    tips.removeClass( "ui-state-highlight", 1500 );
	  }, 500 );
	}

	function checkLength( o, n, min, max ) {
	  if ( o.val().length > max || o.val().length < min ) {
	    o.addClass( "ui-state-error" );
	    updateTips( "Length of " + n + " must be between " +
	      min + " and " + max + "." );
	    return false;
	  } else {
	    return true;
	  }
	}

	function checkRegexp( o, regexp, n ) {
	  if ( !( regexp.test( o.val() ) ) ) {
	    o.addClass( "ui-state-error" );
	    updateTips( n );
	    return false;
	  } else {
	    return true;
	  }
	}

	function addUser() {
	  var valid = true;
	  allFields.removeClass( "ui-state-error" );
	  valid = valid && checkLength( name, "username", 1, 16 );
	  valid = valid && checkRegexp( name, /^[a-z]([0-9a-z_\s])+$/i, "Username may consist of a-z, 0-9, underscores, spaces and must begin with a letter." );

	  if ( valid ) {
	  	$.ajax({
		    url: '/user/',
		    type: 'POST',
		    dataType: 'json',
		    data: {
		        'username':name.val()
		    },
		    success: function(){
		    	alert('success!')
		    	location.reload()
		    },
		    error: function(){
		         alert('failed')
		    }
		})
	    dialog.dialog( "close" );
	  }
	  return valid;
	}

	dialog = $('#dialog-newUser').dialog({
	  autoOpen: false,
	  height: 400,
	  width: 350,
	  modal: true,
	  buttons: {
	    "Create an account": addUser,
	    Cancel: function() {
	      dialog.dialog( "close" );
	    }
	  },
	  	close: function() {
	    form[ 0 ].reset();
	    allFields.removeClass( "ui-state-error" );
	  }
	});

	form = dialog.find( "form" ).on( "submit", function( event ) {
	  event.preventDefault();
	  addUser();
	});

	$( "#create-user" ).button().on( "click", function() {
	  dialog.dialog( "open" );
	});
	$( "#arrange_interview" ).button()
} );
