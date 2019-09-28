// function test_func(data) {
  
//     }

// test_func({{ data|safe }})


document.addEventListener("DOMContentLoaded", function(event) { 
    // your code her  console.log(data);
    var delayInMilliseconds = 3000; //1 second
    var checkExists = setInterval(function() {
        if(data) {
            window.opener.HandlePopupResult(data);
            window.close();
            clearInterval(checkExists);
        }
    }, delayInMilliseconds);
        
  });