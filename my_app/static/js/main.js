jQuery(function(){
    
    let temp, j , i, obj , flag = false;

    jQuery('.calculate-side').on('submit',function(e){
        
        flag = false;
        zero = false;    
        console.log("amount is: ");
        if( jQuery.trim(jQuery('#amount').val())  === "") {
            console.log("no value is entered");
            flag = true;
            temp = 'Please enter amount to invest' ;
        }else if( jQuery.trim(jQuery('#amount').val()) == 0) {
            flag = true;
            temp = 'Please enter amount not equal to 0';
        }else if( jQuery.trim(jQuery('#amount').val()) < 0) {
            flag = true;
            temp = 'Please do not enter negative value and enter amount greater than $5000';
        }else if( jQuery.trim(jQuery('#amount').val()) < 5000 && jQuery.trim(jQuery('#amount').val())!=0 && jQuery.trim(jQuery('#amount').val())>0) {
            flag = true;
            temp = 'Please enter amount greater than $5000';
        } 
        i = 0;
        jQuery('.choiceArea input[type="checkbox"]').each(function(){

             if( jQuery(this).is(':checked') )
                i++;
        });
        if(i > 1) {
             temp = 'You can select only 1 option atmost';
             flag = true;   
        }
         if(flag === false && i === 0) {
             temp = 'Please select an option';
             flag = true;   
        }
        if(flag === true) {
            alert(temp)

            return false; 
       }   
    })
         jQuery('.steps li').each(function(i){
                jQuery(this).css({

                    "-webkit-animation-duration" : (i+0.5)*0.4+"s",
                    "animation-duration" : (i+0.5)*0.4+"s",
                });
         });
         jQuery('.steps li').addClass('fadeInLeft'); 
});


