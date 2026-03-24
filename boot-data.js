// ===== BOOT SIZE DATABASE =====
// Sourced from Long Supply, Home Depot, and common residential sizes

var BOOT_SIZES = {
  // Floor mount boots (90° boots and straight boots)
  floor: {
    label: 'Floor Register',
    sizes: {
      4:  [{reg:'4x10', desc:'4x10 floor'}],
      5:  [{reg:'2-1/4x10', desc:'2-1/4x10 floor'}, {reg:'4x10', desc:'4x10 floor'}],
      6:  [{reg:'2-1/4x10', desc:'2-1/4x10'}, {reg:'2-1/4x12', desc:'2-1/4x12'}, {reg:'2-1/4x14', desc:'2-1/4x14'},
           {reg:'4x10', desc:'4x10'}, {reg:'4x12', desc:'4x12'}, {reg:'4x14', desc:'4x14'},
           {reg:'6x10', desc:'6x10'}, {reg:'6x12', desc:'6x12'}, {reg:'6x14', desc:'6x14'}],
      7:  [{reg:'4x10', desc:'4x10'}, {reg:'4x12', desc:'4x12'}, {reg:'4x14', desc:'4x14'},
           {reg:'6x10', desc:'6x10'}, {reg:'6x12', desc:'6x12'}, {reg:'6x14', desc:'6x14'}],
      8:  [{reg:'4x12', desc:'4x12'}, {reg:'4x14', desc:'4x14'},
           {reg:'6x12', desc:'6x12'}, {reg:'6x14', desc:'6x14'}],
      9:  [{reg:'6x12', desc:'6x12'}, {reg:'6x14', desc:'6x14'}, {reg:'8x14', desc:'8x14'}],
      10: [{reg:'6x14', desc:'6x14'}, {reg:'8x14', desc:'8x14'}, {reg:'8x16', desc:'8x16'}],
      12: [{reg:'8x14', desc:'8x14'}, {reg:'8x16', desc:'8x16'}, {reg:'10x14', desc:'10x14'}],
      14: [{reg:'10x14', desc:'10x14'}, {reg:'10x16', desc:'10x16'}, {reg:'12x14', desc:'12x14'}]
    }
  },
  // Wall mount boots (wall stack boots — 90° angle into wall cavity)
  wall: {
    label: 'Wall Register',
    sizes: {
      4:  [{reg:'10x3-1/4', desc:'10x3-1/4 wall stack'}],
      5:  [{reg:'10x3-1/4', desc:'10x3-1/4'}, {reg:'12x3-1/4', desc:'12x3-1/4'}],
      6:  [{reg:'10x3-1/4', desc:'10x3-1/4'}, {reg:'10x4', desc:'10x4'}, {reg:'12x3-1/4', desc:'12x3-1/4'},
           {reg:'12x4', desc:'12x4'}, {reg:'14x3-1/4', desc:'14x3-1/4'}, {reg:'14x4', desc:'14x4'}],
      7:  [{reg:'12x3-1/4', desc:'12x3-1/4'}, {reg:'12x4', desc:'12x4'},
           {reg:'14x3-1/4', desc:'14x3-1/4'}, {reg:'14x4', desc:'14x4'}],
      8:  [{reg:'12x4', desc:'12x4'}, {reg:'14x4', desc:'14x4'}, {reg:'14x6', desc:'14x6'}],
      9:  [{reg:'14x4', desc:'14x4'}, {reg:'14x6', desc:'14x6'}, {reg:'16x6', desc:'16x6'}],
      10: [{reg:'14x6', desc:'14x6'}, {reg:'16x6', desc:'16x6'}, {reg:'20x6', desc:'20x6'}],
      12: [{reg:'20x6', desc:'20x6'}, {reg:'24x6', desc:'24x6'}, {reg:'20x8', desc:'20x8'}],
      14: [{reg:'24x6', desc:'24x6'}, {reg:'24x8', desc:'24x8'}, {reg:'30x6', desc:'30x6'}]
    }
  },
  // Ceiling mount boots (ceiling diffuser boots — top or side mount)
  ceiling: {
    label: 'Ceiling Diffuser',
    sizes: {
      4:  [{reg:'6x6 sq', desc:'6x6 square diff'}],
      5:  [{reg:'6x6 sq', desc:'6x6 square'}, {reg:'8x8 sq', desc:'8x8 square'}],
      6:  [{reg:'6x6 sq', desc:'6x6 square'}, {reg:'8x8 sq', desc:'8x8 square'},
           {reg:'10x10 sq', desc:'10x10 square'}, {reg:'8 rnd', desc:'8\" round'}],
      7:  [{reg:'8x8 sq', desc:'8x8 square'}, {reg:'10x10 sq', desc:'10x10 square'}, {reg:'8 rnd', desc:'8\" round'}],
      8:  [{reg:'10x10 sq', desc:'10x10 square'}, {reg:'12x12 sq', desc:'12x12 square'},
           {reg:'10 rnd', desc:'10\" round'}, {reg:'8 rnd', desc:'8\" round'}],
      9:  [{reg:'10x10 sq', desc:'10x10'}, {reg:'12x12 sq', desc:'12x12'}, {reg:'10 rnd', desc:'10\" round'}],
      10: [{reg:'12x12 sq', desc:'12x12 square'}, {reg:'14x14 sq', desc:'14x14 square'}, {reg:'12 rnd', desc:'12\" round'}],
      12: [{reg:'14x14 sq', desc:'14x14'}, {reg:'12 rnd', desc:'12\" round'}, {reg:'24x24 lay-in', desc:'24x24 lay-in'}],
      14: [{reg:'24x24 lay-in', desc:'24x24 lay-in'}, {reg:'14 rnd', desc:'14\" round'}]
    }
  },
  // Return grilles
  return: {
    label: 'Return Grille',
    sizes: {
      6:  [{reg:'10x6', desc:'10x6 return'}, {reg:'12x6', desc:'12x6'}],
      8:  [{reg:'12x8', desc:'12x8'}, {reg:'14x8', desc:'14x8'}, {reg:'16x8', desc:'16x8'}],
      10: [{reg:'14x8', desc:'14x8'}, {reg:'16x8', desc:'16x8'}, {reg:'20x8', desc:'20x8'}],
      12: [{reg:'20x8', desc:'20x8'}, {reg:'20x12', desc:'20x12'}, {reg:'24x8', desc:'24x8'}],
      14: [{reg:'20x14', desc:'20x14'}, {reg:'24x12', desc:'24x12'}, {reg:'24x14', desc:'24x14'},
           {reg:'30x12', desc:'30x12'}, {reg:'20x20', desc:'20x20'}],
      16: [{reg:'24x14', desc:'24x14'}, {reg:'24x18', desc:'24x18'}, {reg:'30x14', desc:'30x14'}, {reg:'20x20', desc:'20x20'}],
      18: [{reg:'24x18', desc:'24x18'}, {reg:'30x14', desc:'30x14'}, {reg:'30x18', desc:'30x18'}],
      20: [{reg:'24x24', desc:'24x24'}, {reg:'30x18', desc:'30x18'}, {reg:'30x20', desc:'30x20'}]
    }
  }
};

// Get available boot sizes for a given duct diameter and mount type
function getBootSizes(ductSize, mountType) {
  var cat = BOOT_SIZES[mountType];
  if (!cat) return [];
  var d = parseInt(ductSize);
  // Try exact match first, then closest smaller
  if (cat.sizes[d]) return cat.sizes[d];
  var keys = Object.keys(cat.sizes).map(Number).sort(function(a,b){return a-b;});
  for (var i = keys.length-1; i >= 0; i--) {
    if (keys[i] <= d) return cat.sizes[keys[i]];
  }
  return [];
}
