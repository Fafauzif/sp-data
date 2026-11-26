/** Risk scenarios evaluated through the same operational and financial model. */
const LABELS = {
  seller: "Akuisisi penjual",
  demand: "Permintaan yang memenuhi syarat",
  fee: "Tarif biaya pembeli dan komisi",
  aov: "Nilai barang per pesanan",
  cost: "Biaya operasi",
  completion: "Penyelesaian pesanan",
  capex: "Belanja modal",
};

export const DEFAULT_DRIVERS = Object.freeze({
  // low/mode/high are structured scenario assumptions, not estimates from survey data.
  // Loading order: shared adoption, shared input-cost pressure.
  seller: { bounds: [0.70, 1, 1.24], loadings: [0.65, 0] },
  demand: { bounds: [0.60, 1, 1.35], loadings: [0.70, 0] },
  fee: { bounds: [0.76, 1, 1.18], loadings: [-0.20, 0.10] },
  aov: { bounds: [0.83, 1, 1.16], loadings: [0.32, 0.12] },
  cost: { bounds: [0.89, 1, 1.28], loadings: [0, 0.70] },
  completion: { bounds: [0.77, 1, 1.12], loadings: [0.40, -0.10] },
  capex: { bounds: [0.88, 1, 1.29], loadings: [0, 0.52] },
});

const DISTANCE_TO_ZERO = 1e-11;
const DEFAULT_LEVELS = [0.70, 0.85, 1.00, 1.15, 1.30];
const finite = (v) => typeof v === "number" && Number.isFinite(v);
const moneyEqual = (a, b) => Math.abs(a - b) <= Math.max(1e-8, 1e-9 * Math.max(Math.abs(a), Math.abs(b)));
const sum = (values) => values.reduce((total, value) => total + value, 0);

function seededRandom(seed) {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) | 0;
    let value = Math.imul(state ^ state >>> 15, 1 | state);
    value ^= value + Math.imul(value ^ value >>> 7, 61 | value);
    return ((value ^ value >>> 14) >>> 0) / 4294967296;
  };
}

function gaussianFactory(random) {
  let spare;
  return () => {
    if (spare !== undefined) {
      const result = spare;
      spare = undefined;
      return result;
    }
    const radius = Math.sqrt(-2 * Math.log(Math.max(random(), Number.MIN_VALUE)));
    const angle = 2 * Math.PI * random();
    spare = radius * Math.sin(angle);
    return radius * Math.cos(angle);
  };
}

function normalCdf(value) {
  // Tail approximation error within ~7.5e-8, sufficient for inverse sampling.
  const absolute = Math.abs(value);
  const t = 1 / (1 + 0.2316419 * absolute);
  const tail = Math.exp(-0.5 * absolute ** 2) / Math.sqrt(2 * Math.PI)
    * t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
  return value < 0 ? tail : 1 - tail;
}

function inverseTriangle(u, [low, mode, high]) {
  if (!(low >= 0 && low <= mode && mode <= high && high > low)) {
    throw new Error("Invalid nonnegative triangular range");
  }
  const split = (mode - low) / (high - low);
  return u < split ? low + Math.sqrt(u * (high - low) * (mode - low))
    : high - Math.sqrt((1 - u) * (high - low) * (high - mode));
}

function quantile(sorted, quantileValue) {
  if (sorted.length === 0) return null;
  const i = (sorted.length - 1) * quantileValue;
  const lower = Math.floor(i);
  const upper = Math.ceil(i);
  return sorted[lower] + (sorted[upper] - sorted[lower]) * (i - lower);
}

function percentiles(values) {
  const sorted = values.filter(finite).sort((a, b) => a - b);
  return { n: sorted.length, p05: quantile(sorted, 0.05), p50: quantile(sorted, 0.50), p95: quantile(sorted, 0.95) };
}

function horner(coefficients, x) {
  let value = 0;
  for (let i = coefficients.length - 1; i >= 0; --i) value = value * x + coefficients[i];
  return value;
}

function polynomialSign(coefficients, x) {
  const value = horner(coefficients, x);
  const scale = horner(coefficients.map(Math.abs), x);
  if (Math.abs(value) <= DISTANCE_TO_ZERO * scale) return 0;
  return Math.sign(value);
}

function findRoot(coefficients, low, high, lowSign) {
  for (let iteration = 0; iteration < 61; ++iteration) {
    const middle = (low + high) / 2;
    const sign = polynomialSign(coefficients, middle);
    if (sign === 0 || high - low <= Math.max(1e-15, 1e-12 * middle)) return middle;
    if (sign === lowSign) low = middle;
    else high = middle;
  }
  return (low + high) / 2;
}

function positiveRoots(coefficients) {
  let low = 0;
  let high = coefficients.length;
  while (low < high && coefficients[low] === 0) ++low;
  while (high > low && coefficients[high - 1] === 0) --high;
  const values = coefficients.slice(low, high);
  if (values.length < 2) return [];
  const scale = Math.max(...values.map(Math.abs));
  const normalized = values.map(value => value / scale);
  const nonzeroSigns = normalized.filter(value => value !== 0).map(Math.sign);
  const signChanges = nonzeroSigns.slice(1).filter((sign, index) => sign !== nonzeroSigns[index]).length;
  if (signChanges === 0) return [];
  if (normalized.length === 2) {
    const root = -normalized[0] / normalized[1];
    return root > 0 && finite(root) ? [root] : [];
  }
  if (signChanges === 1) {
    let upper = 1;
    const startSign = Math.sign(normalized[0]);
    while (polynomialSign(normalized, upper) === startSign && upper < 1e30) upper *= 2;
    const endSign = polynomialSign(normalized, upper);
    if (endSign === 0) return [upper];
    if (endSign === startSign) return [];
    return [findRoot(normalized, 0, upper, startSign)];
  }

  // Between consecutive derivative roots, the NPV polynomial is monotonic.
  const bound = 1 + Math.max(...normalized.slice(0, -1).map(value => Math.abs(value / normalized.at(-1))));
  const derivative = normalized.slice(1).map((value, index) => value * (index + 1));
  const critical = positiveRoots(derivative).filter(root => root < bound).sort((a, b) => a - b);
  const edges = [0, ...critical, bound];
  const signs = edges.map(edge => polynomialSign(normalized, edge));
  const roots = critical.filter((_, index) => signs[index + 1] === 0);
  for (let i = 1; i < edges.length; ++i) {
    if (signs[i - 1] * signs[i] === -1) {
      roots.push(findRoot(normalized, edges[i - 1], edges[i], signs[i - 1]));
    }
  }
  return roots.filter(root => root > 0 && finite(root))
    .sort((a, b) => a - b)
    .filter((root, index, ordered) => index === 0 || Math.abs(root / ordered[index - 1] - 1) > 1e-8);
}

export function classifyIrr(cashflows) {
  if (!cashflows.length || !cashflows.every(finite)) throw new Error("Non-finite project FCFF");
  if (cashflows.every(value => value === 0)) return { status: "tidak_terdefinisi", irr: null, roots: [] };
  const roots = positiveRoots(cashflows).map(root => 1 / root - 1).filter(finite).sort((a, b) => a - b);
  const status = roots.length === 1 ? "valid" : roots.length > 1 ? "lebih_dari_satu" : "tidak_tersedia";
  return { status, irr: status === "valid" ? roots[0] : null, roots };
}

function discountedValue(cashflows, hurdle) {
  return sum(cashflows.map((value, time) => value / (1 + hurdle) ** time));
}

function firstCrossing(cashflows, years, hurdle) {
  let signChanges = 0;
  let firstSign = 0;
  let previousSign = 0;
  let cumulativeNpv = 0;
  for (let i = 0; i < cashflows.length; ++i) {
    const cashflow = cashflows[i];
    cumulativeNpv += cashflow / (1 + hurdle) ** i;
    if (cashflow !== 0) {
      const currentSign = Math.sign(cashflow);
      if (previousSign && currentSign !== previousSign) ++signChanges;
      if (!firstSign) firstSign = currentSign;
      previousSign = currentSign;
    }
    if (signChanges === 1 && firstSign < 0 && cumulativeNpv > 1e-8) return years[i];
    if (signChanges > 1 || (signChanges === 1 && firstSign > 0)) {
      const solution = classifyIrr(cashflows.slice(0, i + 1));
      if (finite(solution.irr) && solution.irr - hurdle > 1e-10) return years[i];
    }
  }
  return null;
}

function observe(evaluate, inputs, caseName, multipliers, years, evaluationOptions = {}) {
  const result = evaluate(inputs, { compact: true, ...evaluationOptions, caseName, multipliers });
  if (!result || !Array.isArray(result.annual) || result.annual.length !== years.length
      || !result.annual.every((row, i) => row.year === years[i] && finite(row.fcff))) {
    throw new Error("Operation engine must return one ordered, finite annual FCFF for every target year");
  }
  const hurdle = result.capm;
  if (!finite(hurdle) || hurdle <= -1) throw new Error("Model CAPM is absent or invalid");
  const cashflows = result.annual.map(row => row.fcff);
  const npv = discountedValue(cashflows, hurdle);
  if (!finite(result.npv) || !moneyEqual(npv, result.npv)) {
    throw new Error(`Model NPV (${result.npv}) does not reconcile with FCFF and CAPM (${npv})`);
  }
  const { irr, status } = classifyIrr(cashflows);
  const crossing = firstCrossing(cashflows, years, hurdle);
  const gaps = result.annual.map(row => row.fundingGap).filter(finite);
  const fundingGap = finite(result.fundingGap) ? result.fundingGap
    : gaps.length ? Math.max(0, ...gaps) : null;
  const funding = finite(result.funding) ? result.funding : null;
  const cashMin = finite(result.cashMin) ? result.cashMin : null;
  const cashMinUnfunded = finite(result.cashMinUnfunded) ? result.cashMinUnfunded : null;
  const fundingNeeded = finite(result.fundingNeeded) ? result.fundingNeeded
    : finite(cashMinUnfunded) ? Math.max(0, -cashMinUnfunded) : null;
  const annualEnd = result.annual.at(-1);
  return {
    npv, irr, irrStatus: status, crossing, capm: hurdle, funding, fundingNeeded, cashMin, cashMinUnfunded,
    fundingGap,
    fundingAtRisk: finite(fundingGap) && finite(cashMin) ? (fundingGap > 1e-8 || cashMin < -1e-8) : null,
    endingOrders: annualEnd.orders ?? null,
    capacityLimitedYears: result.annual.every(row => typeof row.capacityLimited === "boolean")
      ? result.annual.filter(row => row.capacityLimited).length : null,
    cashflows,
  };
}

function drawMultipliers(gaussian, drivers) {
  const adoption = gaussian();
  const costs = gaussian();
  return Object.fromEntries(Object.entries(drivers).map(([key, spec]) => {
    const [growth, inflation] = spec.loadings;
    const residualVariance = 1 - growth ** 2 - inflation ** 2;
    if (residualVariance < 0) throw new Error(`Invalid factor loading for ${key}`);
    const draw = growth * adoption + inflation * costs + Math.sqrt(residualVariance) * gaussian();
    return [key, inverseTriangle(normalCdf(draw), spec.bounds)];
  }));
}

function summarize(rows, years) {
  const validIrr = rows.filter(row => row.irrStatus === "valid");
  const measuredFunding = rows.filter(row => row.fundingAtRisk !== null);
  const distribution = Object.fromEntries(years.slice(1).map(year => [year, 0]));
  for (const row of rows) {
    if (row.crossing !== null) ++distribution[row.crossing];
  }
  const countStatus = (status) => rows.filter(row => row.irrStatus === status).length;
  const positiveNpv = rows.filter(row => row.npv > 0).length;
  const overHurdle = validIrr.filter(row => row.irr > row.capm).length;
  return {
    trials: rows.length,
    npv: percentiles(rows.map(row => row.npv)),
    irr: percentiles(validIrr.map(row => row.irr)),
    positiveNpv: { numerator: positiveNpv, denominator: rows.length, probability: positiveNpv / rows.length },
    overHurdle: { numerator: overHurdle, denominator: validIrr.length,
      probability: validIrr.length ? overHurdle / validIrr.length : null, allTrials: rows.length },
    irrUnavailable: countStatus("tidak_tersedia"),
    irrMultiple: countStatus("lebih_dari_satu"),
    irrUndefined: countStatus("tidak_terdefinisi"),
    crossingDistribution: distribution,
    neverCrosses: rows.length - sum(Object.values(distribution)),
    fundedCash: percentiles(rows.map(row => row.cashMin)),
    unfundedCash: percentiles(rows.map(row => row.cashMinUnfunded)),
    funding: percentiles(rows.map(row => row.funding)),
    fundingNeeded: percentiles(rows.map(row => row.fundingNeeded)),
    fundingGap: percentiles(rows.map(row => row.fundingGap)),
    fundingRisk: {
      numerator: measuredFunding.filter(row => row.fundingAtRisk).length,
      denominator: measuredFunding.length,
      probability: measuredFunding.length
        ? measuredFunding.filter(row => row.fundingAtRisk).length / measuredFunding.length : null,
    },
  };
}

function histogram(rows, key, nBins = 15) {
  const values = rows.map(row => row[key]).filter(finite);
  if (!values.length) return [];
  const low = Math.min(...values);
  const high = Math.max(...values);
  if (low === high) return [{ low, high, count: values.length }];
  const bins = Array.from({ length: nBins }, (_, index) => ({
    low: low + (high - low) * index / nBins,
    high: low + (high - low) * (index + 1) / nBins,
    count: 0,
  }));
  for (const value of values) {
    ++bins[Math.min(nBins - 1, Math.floor((value - low) / (high - low) * nBins))].count;
  }
  return bins;
}

function pearson(pairs) {
  if (pairs.length < 2) return null;
  const averages = [0, 1].map(index => sum(pairs.map(pair => pair[index])) / pairs.length);
  let covariance = 0;
  let spreadX = 0;
  let spreadY = 0;
  for (const [x, y] of pairs) {
    const xDelta = x - averages[0];
    const yDelta = y - averages[1];
    covariance += xDelta * yDelta;
    spreadX += xDelta ** 2;
    spreadY += yDelta ** 2;
  }
  return spreadX && spreadY ? covariance / Math.sqrt(spreadX * spreadY) : null;
}

export function sensitivity({ evaluate, inputs, years, levels = DEFAULT_LEVELS, evaluationOptions = {} }) {
  if (levels.length % 2 !== 1 || levels[Math.floor(levels.length / 2)] !== 1
      || levels.some((value, index) => !finite(value) || value <= 0 || (index > 0 && levels[index - 1] >= value))) {
    throw new Error("Sensitivity levels must strictly increase and be centered on 1.00");
  }
  const center = observe(evaluate, inputs, "Base", {}, years, evaluationOptions);
  const cells = levels.map(demand => levels.map(fee => {
    const outcome = observe(evaluate, inputs, "Base", { demand, fee }, years, evaluationOptions);
    return { demand, fee, ...outcome };
  }));
  const midpoint = cells[Math.floor(levels.length / 2)][Math.floor(levels.length / 2)];
  if (!moneyEqual(center.npv, midpoint.npv) || center.irrStatus !== midpoint.irrStatus
      || (finite(center.irr) && !moneyEqual(center.irr, midpoint.irr))) {
    throw new Error("Sensitivity center does not reproduce Base");
  }
  const feeBreakEven = levels.map((demand, index) => {
    const values = cells[index];
    const points = [];
    for (let i = 0; i < values.length; ++i) {
      const current = values[i];
      if (current.npv === 0) points.push(current.fee);
      if (i === 0) continue;
      const prior = values[i - 1];
      if (prior.npv * current.npv < 0) {
        // Report a model-recomputed bracket and a bracketed threshold to 0.001x tariff.
        let a = prior.fee;
        let b = current.fee;
        const sign = Math.sign(prior.npv);
        while (b - a > 0.001) {
          const fee = (a + b) / 2;
          const value = observe(evaluate, inputs, "Base", { demand, fee }, years, evaluationOptions).npv;
          if (Math.sign(value) === sign) a = fee;
          else b = fee;
        }
        points.push((a + b) / 2);
      }
    }
    return { demand, points, lowerNpv: values[0].npv, upperNpv: values.at(-1).npv };
  });
  return { levels, center, cells, feeBreakEven, startYear: years[0], assessmentYear: years.at(-1) };
}

export function simulate({
  evaluate, inputs, years, selector = "Base", seed = 12026, n = 10000, drivers = DEFAULT_DRIVERS,
  evaluationOptions = {},
}) {
  if (!Number.isSafeInteger(seed) || seed < 0 || seed > 0xffffffff) throw new Error("Seed must be a 32-bit unsigned integer");
  if (!Number.isSafeInteger(n) || n < 1 || n > 100000) throw new Error("Trial count must be between 1 and 100,000");
  if (!Array.isArray(years) || years.length < 2 || years.some((year, i) => !Number.isInteger(year)
      || (i > 0 && year - years[i - 1] !== 1))) throw new Error("Risk model requires consecutive annual periods");
  const baseline = observe(evaluate, inputs, selector, {}, years, evaluationOptions);
  const gaussian = gaussianFactory(seededRandom(seed));
  const rows = Array.from({ length: n }, (_, index) => {
    const multipliers = drawMultipliers(gaussian, drivers);
    return { id: index + 1, multipliers, ...observe(evaluate, inputs, selector, multipliers, years, evaluationOptions) };
  });
  const factorCorrelations = Object.fromEntries(Object.keys(drivers).map(a =>
    [a, Object.fromEntries(Object.keys(drivers).map(b => [b, a === b ? 1 :
      sum(drivers[a].loadings.map((value, index) => value * drivers[b].loadings[index]))]))]));
  const riskDrivers = Object.keys(drivers).map(key => ({
    key, label: LABELS[key] ?? key,
    npvCorrelation: pearson(rows.map(row => [row.multipliers[key], row.npv])),
    fundingGapCorrelation: pearson(rows.filter(row => finite(row.fundingGap))
      .map(row => [row.multipliers[key], row.fundingGap])),
  })).sort((a, b) => Math.abs(b.npvCorrelation ?? 0) - Math.abs(a.npvCorrelation ?? 0));
  const half = Math.floor(n / 2);
  return {
    seed, n, selector, years, evaluationOptions, assessmentYear: years.at(-1),
    method: "Kopula Gaussian dua faktor dengan marginal triangular terikat. Pengali driver tetap per trial selama horizon. CAPM tetap mengikuti model.",
    factorNames: ["Adopsi bersama", "Tekanan biaya input"],
    drivers: Object.fromEntries(Object.entries(drivers).map(([key, spec]) => [key, { ...spec, label: LABELS[key] ?? key }])),
    factorCorrelations, baseline, rows,
    summary: summarize(rows, years),
    stability: half > 0 ? {
      firstHalf: summarize(rows.slice(0, half), years),
      secondHalf: summarize(rows.slice(half), years),
    } : null,
    riskDrivers,
    npvHistogram: histogram(rows, "npv"),
    gapHistogram: histogram(rows, "fundingGap"),
  };
}
