
window.resizeGraph = function() {
  var g = $('#graph');
  g.attr('width',g.width()).attr('height',g.height());
};

// Resize graph on load
window.preload = function() {
  resizeGraph();
  $(window).resize(resizeGraph);
}

window._palette = 0;
window.paletteColor = function() {
  var colz = [
   '#00A0B0',
   '#6A4A3C',
   '#CC333F',
   '#EB6841',
   '#EDC951',
   '#7DBE3C',
   '#000000',
   '#00A0B0',
   '#6A4A3C',
   '#CC333F',
   '#EB6841',
 ];
  return colz[ _palette++ % colz.length ];
}
