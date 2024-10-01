document.getElementById("page").addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    var inputValue = document.getElementById('page').value;
    var page = 1;
    if (inputValue === '') {page = 1} else {page = inputValue}
    window.location.href = "/vehicles?page="+page+"&search="+document.getElementById('search').value;
  }
});
document.getElementById("search").addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    var inputValue = document.getElementById('search').value;
    var searchv = "";
    if (inputValue === '') {searchv = ''} else {searchv = inputValue}
    window.location.href = "/vehicles?page="+document.getElementById('page').value+"&search="+searchv;
  }
});
function dowloadprocess(){
  document.getElementById('window').style.display = 'block';
  document.getElementById('background').style.display = 'block';
}