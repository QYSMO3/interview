var dialog_newUser, dialog_interview,form,
name = $( "#name"),
tips = $( ".validateTips" );

function updateTips( t ) {
  tips
    .text( t )
    .addClass( "ui-state-highlight" );
  setTimeout(function() {
    tips.removeClass( "ui-state-highlight", 1500 );
  }, 500 );
}

// function checkLength( o, n, min, max ) {
//   if ( o.val().length > max || o.val().length < min ) {
//     o.addClass( "ui-state-error" );
//     updateTips( "Length of " + n + " must be between " +
//       min + " and " + max + "." );
//     return false;
//   } else {
//     return true;
//   }
// }

// function checkRegexp( o, regexp, n ) {
//   if ( !( regexp.test( o.val() ) ) ) {
//     o.addClass( "ui-state-error" );
//     updateTips( n );
//     return false;
//   } else {
//     return true;
//   }
// }

function addUser() {
  var valid = true;
  // valid = valid && checkLength( name, "username", 1, 16 );
  // valid = valid && checkRegexp( name, /^[a-z]([0-9a-z_\s])+$/i, "Username may consist of a-z, 0-9, underscores, spaces and must begin with a letter." );

  if ( valid ) {
  	$.ajax({
	    url: '/user/',
	    type: 'POST',
	    dataType: 'json',
	    data: {
	        'username':$("#username")[0].value
	    },
	    success: function(){
	    	alert('Success!')
	    	location.reload()
	    },
	    error: function(){
	         alert('Failed')
	    }
	})
    dialog_newUser.dialog( "close" );
  }
  return valid;
}

dialog_newUser = $('#dialog-newUser').dialog({
  autoOpen: false,
  height: 400,
  width: 350,
  modal: true,
  buttons: {
    "Create an account": addUser,
    Cancel: function() {
      dialog_newUser.dialog( "close" );
    }
  },
  	close: function() {
    form[ 0 ].reset();
  }
});

form = dialog_newUser.find( "form" ).on( "submit", function( event ) {
  event.preventDefault();
  addUser();
});

$( "#create-user" ).button().on( "click", function() {
  dialog_newUser.dialog("open");
});
$( "[name='arrange_interview']" ).button()



function arrange(opt){
	selects = $("select[name='s_interview']");
	var c=new Array;
	var i=new Array;
	$.each(selects, function(){ 
		var id =this.id.substring(this.id.indexOf('_')+1,this.id.length)   
    	if (this.value==1){
    		c.push(id)
    	}else if (this.value==2){
    		i.push(id)
    	}
    });
	if (opt==1){
		$.ajax({
		    url: '/interviews/',
		    type: 'POST',
		    dataType: 'json',
		    traditional: true,
		    data: {
		        'c':c,
		        'i':i,
		    },
		    success: function(data){
		    	alert('Success!')
		    	$('#r_get').html(JSON.stringify(data))
		    },
		    error: function(error){
		    	alert('Failed!')
		        $('#r_get').html(error.responseText)
		    }
		})  
	}else{
		$.ajax({
		    url: '/available_times/',
		    type: 'GET',
		    dataType: 'json',
		    traditional: true,
		    data: {
		        'c':c,
		        'i':i,
		    },
		    success: function(data){
		    	$('#r_get').html(JSON.stringify(data))
		    },
		    error: function(error){
		        $('#r_get').html(error.responseText)
		    }
		})  
	}
  
}
