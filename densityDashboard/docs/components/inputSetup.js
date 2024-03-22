import * as Inputs from "npm:@observablehq/inputs";

export function leaseAreaPicker(densityData) {

    const leaseAreas = [... new Set(densityData.map(d => d.lease_area))];

    const leaseAreaPick = Inputs.select(
        [null].concat(leaseAreas),
        {
            value: "OCS-A 0482 - GSOE I  LLC",
            label: "Lease Area"
        });

    return leaseAreaPick;

}


export function leaseAreaPicker(densityData) {

    const speciesNames = [... new Set(densityData.map(d => d.species))];

    const speciesPick = Inputs.select(speciesNames, { label: "Species" });

    return speciesPick;

}
