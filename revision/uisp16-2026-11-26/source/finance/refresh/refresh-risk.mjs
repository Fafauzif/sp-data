import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import fs from "node:fs/promises";
import path from "node:path";
import {evaluate,defaults,years} from "./fin-model.mjs";
import {simulate,sensitivity} from "./simulation.mjs";

const [inputFile,outputFolder,updatedWorkbook]=process.argv.slice(2);
if(!inputFile||!outputFolder){
  process.stderr.write("Pemakaian: node refresh-risk.mjs model.xlsx folder-keluaran [nama-xlsx-baru]\n");
  process.exit(2);
}
const file = f => fileURLToPath(new URL(f,import.meta.url));
const reader = process.env.CODEX_PRIMARY_RUNTIME_PYTHON ?? "python3";
const inputs = {...defaults,...JSON.parse(execFileSync(reader,[file("read-inputs.py"),inputFile],{encoding:"utf8"}))};
const run = (i,o)=>evaluate(i,{...o,compact:true});
const risks={simulation:simulate({evaluate:run,inputs,years,n:10000,seed:12026}),
  sensitivity:sensitivity({evaluate:run,inputs,years})};
await fs.mkdir(outputFolder,{recursive:true});
const inputsPath=path.resolve(outputFolder,"Asumsi_Yang_Digunakan.json");
const riskPath=path.resolve(outputFolder,"Risiko_Diperbarui.json");
await fs.writeFile(inputsPath,JSON.stringify(inputs,null,2));
await fs.writeFile(riskPath,JSON.stringify(risks));
const csv=v=>v==null?"":typeof v==="number"?String(v):'"'+String(v).replaceAll('"','""')+'"';
const writeCSV=(name,records)=>fs.writeFile(path.join(outputFolder,name),
  "\ufeff"+records.map(r=>r.map(csv).join(",")).join("\r\n")+"\r\n");
const {simulation,sensitivity:sens}=risks;
const multipliers=Object.keys(simulation.rows[0].multipliers);
await writeCSV("Monte_Carlo_10000.csv",[
 ["trial",...multipliers,"NPV Rp juta","IRR","Status IRR","Tahun crossing","CAPM","Pendanaan Rp juta","Kas min","Kas min tanpa pendanaan","Funding gap","Pesanan 2036",...years],
 ...simulation.rows.map(q=>[q.id,...multipliers.map(k=>q.multipliers[k]),q.npv,q.irr,q.irrStatus,q.crossing,q.capm,q.funding,q.cashMin,q.cashMinUnfunded,q.fundingGap,q.endingOrders,...q.cashflows])
]);
await fs.writeFile(path.join(outputFolder,"Ringkasan_Risiko.json"),JSON.stringify({summary:simulation.summary,sensitivity:sens},null,2));
if(updatedWorkbook){
  execFileSync(process.env.CODEX_PRIMARY_RUNTIME_NODE??process.execPath,[file("fin-workbook.mjs")],{
    env:{...process.env,LIHATDULU_TARGET:path.resolve(updatedWorkbook),LIHATDULU_INPUTS:inputsPath,LIHATDULU_RISK:riskPath},
    stdio:"inherit"
  });
}
console.log("Pengujian ulang selesai",outputFolder);
