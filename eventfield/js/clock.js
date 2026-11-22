const SLOPE_GYR = 0.52;
const INTERCEPT_GYR = -0.24;
const FIT_MIN = 1;
const FIT_MAX = 3.5;

export function clockFit(ratio) {
  return ratio >= FIT_MIN && ratio <= FIT_MAX ? SLOPE_GYR * ratio + INTERCEPT_GYR : null;
}

export function projectionExample(angleDeg, ratio = 2.4) {
  const projected = ratio * Math.cos(angleDeg * Math.PI / 180);
  const reference = clockFit(ratio);
  const projectedReading = clockFit(projected);
  return {
    ratio, projected, reference, projectedReading,
    shiftMyr: projectedReading === null || reference === null ? null : 1000 * (projectedReading - reference),
  };
}

export function clockSensitivityMyr(distanceShiftKpc, radiusKpc) {
  if (radiusKpc <= 0) throw new RangeError("R500c must be positive");
  return 1000 * SLOPE_GYR * distanceShiftKpc / radiusKpc;
}
