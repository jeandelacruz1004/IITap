function checkDate(testData) {
    let today = new Date().toISOString().slice(0, 10);

    if (testData == today) {
        alert("This event is this day");
    }
    else {
        alert("This event is not today mate");
        console.log(`The date today is ${today} while the event date clicked is ${testData}`);
    
    }

}