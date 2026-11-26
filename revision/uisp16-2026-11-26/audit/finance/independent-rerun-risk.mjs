import fs from 'node:fs/promises';
import { evaluate, defaults, years } from './fin-model.mjs';
import { simulate, sensitivity } from './simulation.mjs';
const old=JSON.parse(await fs.readFile('/tmp/ldfin/risk.json','utf8'));
const simulation=simulate({evaluate,inputs:defaults,years,seed:old.simulation.seed,n:old.simulation.n,selector:old.simulation.selector});
const grids=sensitivity({evaluate,inputs:defaults,years});
const delta = simulation.rows.map((value,i)=>value.fundingGap-old.simulation.rows[i].fundingGap);
console.log(JSON.stringify({
 oldGap:old.simulation.summary.fundingGap, newGap:simulation.summary.fundingGap,
 oldRisk:old.simulation.summary.fundingRisk, newRisk:simulation.summary.fundingRisk,
 nChangedMonthlyGap:delta.filter(v=>Math.abs(v)>1e-6).length, maxAbsGapDelta:Math.max(...delta.map(Math.abs)),
 maxAbsNpvDelta:Math.max(...simulation.rows.map((value,i)=>Math.abs(value.npv-old.simulation.rows[i].npv))),
 baseFundingGap:grids.center.fundingGap,
},null,2));
await fs.writeFile('/tmp/ldfin/risk-monthly-gap.json', JSON.stringify({simulation,sensitivity:grids}));
