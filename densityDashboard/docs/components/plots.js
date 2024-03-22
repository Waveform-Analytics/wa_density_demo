import * as Plot from "npm:@observablehq/plot";


export function species_plot(density_data, leaseAreaPick, speciesPick, { width }) {

    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    const statsSummaryFiltered2 = density_data.filter(item => item.lease_area === leaseAreaPick && item.species === speciesPick);

    const newSummary = statsSummaryFiltered2;

    newSummary.forEach(
        item => {
            item.month_name = monthNames[item.month - 1];
        });

    newSummary.forEach(
        item => { item.species_name = item.species.replace(/_/g, ' ') }
    );

    const speciesPlot = Plot.plot({
        title: `Monthly density: ${speciesPick.replace(/_/g, ' ')}`,
        subtitle: `Lease area: ${leaseAreaPick}`,
        x: { domain: monthNames, label: "Month" },
        y: { grid: true, label: "Animals per 100 km^2" },
        height: 400,
        width,
        marginLeft: 50,
        color: { legend: true, scheme: "Tableau10" },
        marks: [
            Plot.lineY(newSummary, {
                x: "month_name",
                y: "density",
                stroke: "buffer_size",
                marker: true,
                tip: {
                    format: {
                        species: true,
                        buffer_size: true,
                        stroke: false
                    }
                }
            }),
            Plot.ruleY([0]),
        ]
    });

    return speciesPlot;

}


export function monthly_plot(density_data, leaseAreaPick, buff, { width }) {

    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const overlap = 1.5;
    const statsSummaryFiltered = density_data.filter(item => item.lease_area === leaseAreaPick && item.buffer_size === buff);

    const speciesGroups = statsSummaryFiltered.reduce((acc, d) => {
        if (!acc[d.species]) {
            acc[d.species] = [];
        }
        acc[d.species].push(d);
        return acc;
    }, {});

    // Calculate the maximum density for each species
    const maxDensityBySpecies = {};
    for (const species in speciesGroups) {
        maxDensityBySpecies[species] = Math.max(...speciesGroups[species].map(d => d.density));
    };

    //Scale the density for each entry
    const scaledStatsSummary = statsSummaryFiltered.map(d => ({
        ...d,
        scaledDensity: d.density / maxDensityBySpecies[d.species]
    }));

    // Add a month name (not just a number)
    scaledStatsSummary.forEach(
        item => {
            item.month_name = monthNames[item.month - 1];
        })

    // Add a species name column where there are spaces rather than underscores between words
    scaledStatsSummary.forEach(
        item => { item.species_name = item.species.replace(/_/g, ' ') }
    )

    const month_plot = Plot.plot({
        title: "Monthly average species presence",
        subtitle: "Average monthly prescence of different species near offshore wind lease areas",
        height: 200 + new Set(scaledStatsSummary.map(d => d.species)).size * 15,
        width,
        marginBottom: 1,
        marginLeft: 155,
        color: { scheme: "Tableau10" },
        x: { axis: "top", domain: monthNames, label: "Month", },
        y: { axis: null, range: [2.5 * 17 - 2, (2.5 - overlap) * 17 - 2] },
        fy: { label: null, domain: scaledStatsSummary.map(d => d.species_name) },
        marks: [
            Plot.areaY(scaledStatsSummary, {
                x: "month_name", y: "scaledDensity", fy: "species_name", curve: "basis", sort: "month",
                fill: "species_name"
            }),
            Plot.lineY(scaledStatsSummary, {
                x: "month_name", y: "scaledDensity", fy: "species_name", curve: "basis", sort: "month",
                strokeWidth: 1, stroke: "species_name"
            }),
        ]
    });
    return month_plot;
}