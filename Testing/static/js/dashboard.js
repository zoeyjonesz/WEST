async function fetchAndUpdate() {
    const res = await fetch("/simulate");
    const data = await res.json();
  
    // Update tank visuals and log
    tanks.bta.volume = data.bta.volume;
    tanks.btb.volume = data.btb.volume;
    tanks.recycle.volume = data.recycle.volume;
  
    document.getElementById("btaValveState").textContent = `Valve: ${data.bta.valve}`;
    document.getElementById("btbValveState").textContent = `Valve: ${data.btb.valve}`;
    document.getElementById("compressorSpeedLabel").textContent = `${data.recycle.compressor_speed}%`;
    document.getElementById("methaneOutput").textContent = `${data.recycle.methane_output} m³/s`;
  
    updateTankVisual(tanks.bta.volume, tanks.bta.max, 'btaBar', 'btaLabel', 'btaPressure');
    updateTankVisual(tanks.btb.volume, tanks.btb.max, 'btbBar', 'btbLabel', 'btbPressure');
    updateRecycle();
  }
  
  setInterval(fetchAndUpdate, 1000); // Live update every second
  