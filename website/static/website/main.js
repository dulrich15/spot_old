function Toggle(id) 
{
  e = document.getElementById(id).style;
  e.display = ( e.display != 'none' ) ? 'none' : 'block';
}