function loginToSchoolSite(){
  var ss = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Login'); // Name the sheet as 'Login'
  var url = "http://classroom.dwit.edu.np/login/index.php";
  var payload = {
    "username":"", // Classroom site's username and password
    "password":""  
  };
  
  var opt = {
    "payload":payload,
    "method":"post",
    "followRedirects" : false
  };
  
  var response = UrlFetchApp.fetch(encodeURI(url),opt);
  
  if ( response.getResponseCode() == 200 ) {
    var result = "Couldn't login. Please make sure your username/password is correct."; }
  else if ( response.getResponseCode() == 303 ) {
    var result = "Logged in successfully";
    var cookie = response.getAllHeaders()['Set-Cookie'];
    
  var header = {
      'Cookie':cookie[1]
  };
 
  var opt2 = {
    "headers":header
  };
  
  var assignment_url = UrlFetchApp.fetch("http://classroom.dwit.edu.np/mod/assign/index.php?id=37",opt2).getContentText(); // change id according to the subject
  var doc = Xml.parse(assignment_url, true);
  var bodyHtml = doc.html.body.toXmlString();
  doc = XmlService.parse(bodyHtml);
  var html = doc.getRootElement();
  
  var table = getElementsByClassName(html, 'generaltable')[0];
  var tbody = getElementsByTagName(table, 'tbody')[0];
  
  var week = getElementsByClassName(tbody, 'cell c0');
  var assignments = getElementsByClassName(tbody, 'cell c1');
  var due_date = getElementsByClassName(tbody, 'cell c2');
  var submission = getElementsByClassName(tbody, 'cell c3');
  
  for (var i in week){ // View logger for details. View ->Logs.
    Logger.log(week[i].getText());
    Logger.log(assignments[i].getValue());
    Logger.log(due_date[i].getText());
    Logger.log(submission[i].getText());
  } 
  }
  
}

function getElementsByClassName(element, classToFind) {  
  var data = [];
  var descendants = element.getDescendants();
  descendants.push(element);  
  for(i in descendants) {
    var elt = descendants[i].asElement();
    if(elt != null) {
      var classes = elt.getAttribute('class');
      if(classes != null) {
        classes = classes.getValue();
        if(classes == classToFind) data.push(elt);
        else {
          classes = classes.split(' ');
          for(j in classes) {
            if(classes[j] == classToFind) {
              data.push(elt);
              break;
            }
          }
        }
      }
    }
  }
  return data;
}


function getElementsByTagName(element, tagName) {  
  var data = [];
  var descendants = element.getDescendants();  
  for(i in descendants) {
    var elt = descendants[i].asElement();     
    if( elt !=null && elt.getName()== tagName) data.push(elt);      
  }
  return data;
}
