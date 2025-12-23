// Toggle heatmap view
const heatmapToggle = document.getElementById('heatmap-toggle');
const tableWrap = document.querySelector('.table-wrap');
let heatmapActive = false;

heatmapToggle.addEventListener('click', function() {
  heatmapActive = !heatmapActive;
  tableWrap.classList.toggle('heatmap-mode', heatmapActive);
  
  // Toggle heatmap colors on all cells
  document.querySelectorAll('.cell').forEach(cell => {
    if (heatmapActive && !cell.classList.contains('empty')) {
      const color = cell.dataset.heatmapColor;
      cell.style.backgroundColor = color;
    } else {
      // Restore original class-based colors
      cell.style.backgroundColor = '';
    }
  });
    // Toggle legend rows and EN scale display (keep the legend box in place)
    const legendArea = document.querySelector('.legend-area');
    const enScale = document.getElementById('en-scale');
    const legendRows = legendArea.querySelectorAll('.legend-row');
    if (heatmapActive) {
      legendRows.forEach(r => r.style.display = 'none');
      if (enScale) enScale.style.display = 'flex';
    } else {
      legendRows.forEach(r => r.style.display = 'flex');
      if (enScale) enScale.style.display = 'none';
    }
  
  
  // Update button text
  heatmapToggle.textContent = heatmapActive ? 'Show Default Table' : 'Show Electronegativity Heatmap';
});

// Element click handler (fetch details)
document.addEventListener('click', function(e) {
  const cell = e.target.closest('.cell');
  if (!cell || cell.classList.contains('empty')) return;
  const sym = cell.dataset.symbol;
  fetch(`/api/element/${sym}`)
    .then(r => r.json())
    .then(res => {
      const info = document.getElementById('info');
      if (!res.success) { info.textContent = res.error || 'Error'; return; }
      const d = res.data;
      info.innerHTML = `<b>${d.name} (${d.symbol})</b>\nAtomic Number: ${d.atomic_number}\nAtomic Weight: ${d.atomic_weight}\nPeriod: ${d.period}  Group: ${d.group}\nBlock: ${d.block}\nElectronegativity: ${d.en_pauling}\nDensity: ${d.density}\nAtomic Radius: ${d.atomic_radius}\n\n${d.description}\nSeries: ${d.series_name}`;
    })
    .catch(err => { document.getElementById('info').textContent = 'Fetch error: '+err; });
});
