var popupWindow = null;
function centeredPopup(url,winName,w,h,scroll){
    LeftPosition = (screen.width) ? (screen.width-w)/2 : 0;
    TopPosition = (screen.height) ? (screen.height-h)/2 : 0;
    settings =
    'height='+h+',width='+w+',top='+TopPosition+',left='+LeftPosition+',scrollbars='+scroll+',resizable'
    popupWindow = window.open(url,winName,settings)
    popupWindow.focus();
}

function HandlePopupResult(myVal)
{
    document.getElementById('studentUID').value = myVal;
}

function closePopup(){
    window.close();
}

function HandlePictureResult(myVal){ 
    document.getElementById('profile-pic').src = myVal;
    document.getElementById('profile-val').value = myVal;
}