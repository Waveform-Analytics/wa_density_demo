---
toc: false
---

```js
import {monthly_plot, species_plot} from "./components/plots.js";

```

<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 6rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 2rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>


<div class="hero">
  <h1>Marine mammal density explorer</h1>
  <h2>Explore variations in monthly species density near offshore wind lease areas</h2>
</div>


<div class="grid grid-cols-2";>

  <div class="card">
  <h2><b>Overview</b></h2>

  To use this dashboard, you will first need to select a lease area. This will be used for both of the plots. 
  
  The first plot allows you to explore how species presence changes over the course of the year. You have the additional option to choose different buffer sizes around the lease area. 
  
  The second plot focuses in on a single species, so that you can directly compare the differences arising from different buffer sizes. 
  </div>


  <div class="card">
  <h1>Select a lease area</h1>

  The lease area that you select here controls both of the plots on this dashboard. These lease areas are based on files downloaded from the BOEM website. 

  ${leaseAreaInput}
  </div>




</div>


<div class="grid grid-cols-2" style="grid-auto-rows: 504;">

  <div class="card">
  ${bufferInput}

  ${resize((width) => monthly_plot(density, leaseAreaPick, bufferPick, {width}))}
    
  </div>


  <div class="card">
  ${speciesInput}
  
  ${resize((width) => species_plot(density, leaseAreaPick, speciesPick, {width}))}

  </div>
</div>


```js
const density = FileAttachment("data/stats_summary.csv").csv({typed: true});
```

```js
const leaseAreas = [... new Set(density.map(d => d.lease_area))];
const leaseAreaInput = Inputs.select(leaseAreas, {label: "Lease Area", width:400});
const leaseAreaPick = Generators.input(leaseAreaInput);

```

```js
const speciesNames = [... new Set(density.map(d => d.species))];
const speciesInput = Inputs.select(speciesNames, 
{ 
  label: "Species",
  format: (s) => `${s.replace(/_/g, ' ')}`

});
const speciesPick = Generators.input(speciesInput);

```

```js
const bufferSizes = [... new Set(density.map(d => d.buffer_size))];
const bufferInput = Inputs.select(bufferSizes, 
{ 
  label: "Buffer size (m)",
  format: (b) => `${b / 1000} km`

});
const bufferPick = Generators.input(bufferInput);

```
