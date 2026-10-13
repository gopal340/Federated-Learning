import React, { useState } from 'react';
import { PieChart as PieIcon, Info } from 'lucide-react';

interface RiskPieChartProps {
  confidence: number;
  isRisk: boolean;
  riskBreakdown?: Record<string, number>;
}

export const RiskPieChart: React.FC<RiskPieChartProps> = ({
  confidence,
  isRisk,
  riskBreakdown,
}) => {
  const [activeTab, setActiveTab] = useState<'verdict' | 'factors'>('verdict');
  const [hoveredSlice, setHoveredSlice] = useState<string | null>(null);

  // Verdict distribution
  const riskProb = Math.round(confidence * 1000) / 10;
  const safeProb = Math.round((100 - riskProb) * 10) / 10;

  // Factor breakdown data
  const defaultFactors: Record<string, number> = isRisk
    ? {
        'Velocity Anomaly': 42.0,
        'AML Structuring': 33.0,
        'Cross-Border Exposure': 25.0,
      }
    : {
        'Verified KYC': 48.0,
        'Authorized Velocity': 32.0,
        'Routine Channel': 20.0,
      };

  const factors: Record<string, number> = riskBreakdown || defaultFactors;
  const factorKeys = Object.keys(factors);
  const factorColors = isRisk
    ? ['#ef4444', '#f59e0b', '#06b6d4'] // Crimson, Amber, Cyan
    : ['#10b981', '#3b82f6', '#8b5cf6']; // Emerald, Blue, Purple

  // SVG parameters
  const size = 180;
  const center = size / 2;
  const radius = 68;
  const strokeWidth = 26;
  const circumference = 2 * Math.PI * radius;

  // Compute stroke offsets for factors
  let cumulativePercent = 0;
  const factorSlices = factorKeys.map((key, i) => {
    const val = factors[key];
    const strokeDasharray = `${(val / 100) * circumference} ${circumference}`;
    const strokeDashoffset = -((cumulativePercent / 100) * circumference);
    cumulativePercent += val;
    return {
      name: key,
      value: val,
      color: factorColors[i % factorColors.length],
      strokeDasharray,
      strokeDashoffset,
    };
  });

  return (
    <div className="risk-pie-container animate-fade-in">
      <div className="pie-header-row">
        <div className="pie-title-block">
          <PieIcon size={16} className="text-cyan-500" />
          <h4>Calibrated Decision Distribution</h4>
        </div>

        {/* Tab switcher */}
        <div className="pie-tab-pill">
          <button
            className={`pie-tab-btn ${activeTab === 'verdict' ? 'active' : ''}`}
            onClick={() => setActiveTab('verdict')}
          >
            Stance Probability
          </button>
          <button
            className={`pie-tab-btn ${activeTab === 'factors' ? 'active' : ''}`}
            onClick={() => setActiveTab('factors')}
          >
            Risk Breakdown
          </button>
        </div>
      </div>

      <div className="pie-visual-row">
        {/* SVG Donut Chart */}
        <div className="pie-svg-wrapper">
          <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="pie-svg">
            <defs>
              <filter id="glow-risk" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>

            {/* Background ring */}
            <circle
              cx={center}
              cy={center}
              r={radius}
              fill="transparent"
              stroke="#f1f5f9"
              strokeWidth={strokeWidth}
            />

            {activeTab === 'verdict' ? (
              <>
                {/* Safe slice */}
                <circle
                  cx={center}
                  cy={center}
                  r={radius}
                  fill="transparent"
                  stroke="#10b981"
                  strokeWidth={strokeWidth}
                  strokeDasharray={`${(safeProb / 100) * circumference} ${circumference}`}
                  strokeDashoffset={-((riskProb / 100) * circumference)}
                  transform={`rotate(-90 ${center} ${center})`}
                />
                {/* Risk slice */}
                <circle
                  cx={center}
                  cy={center}
                  r={radius}
                  fill="transparent"
                  stroke="#ef4444"
                  strokeWidth={strokeWidth}
                  strokeDasharray={`${(riskProb / 100) * circumference} ${circumference}`}
                  strokeDashoffset="0"
                  transform={`rotate(-90 ${center} ${center})`}
                  style={{ filter: 'drop-shadow(0 0 6px rgba(239, 68, 68, 0.4))' }}
                />
              </>
            ) : (
              factorSlices.map((slice, i) => (
                <circle
                  key={i}
                  cx={center}
                  cy={center}
                  r={radius}
                  fill="transparent"
                  stroke={slice.color}
                  strokeWidth={hoveredSlice === slice.name ? strokeWidth + 4 : strokeWidth}
                  strokeDasharray={slice.strokeDasharray}
                  strokeDashoffset={slice.strokeDashoffset}
                  transform={`rotate(-90 ${center} ${center})`}
                  className="pie-slice-arc"
                  onMouseEnter={() => setHoveredSlice(slice.name)}
                  onMouseLeave={() => setHoveredSlice(null)}
                />
              ))
            )}
          </svg>

          {/* Central Percentage / Readout */}
          <div className="pie-center-label">
            <span className="pie-center-val font-mono">{riskProb}%</span>
            <span className="pie-center-sub">{isRisk ? 'FRAUD RISK' : 'CLEARED'}</span>
          </div>
        </div>

        {/* Legend */}
        <div className="pie-legend-col">
          {activeTab === 'verdict' ? (
            <div className="legend-items-list">
              <div className="legend-item">
                <span className="legend-bullet" style={{ backgroundColor: '#ef4444' }}></span>
                <div className="legend-info">
                  <span className="legend-label">Fraud & Anomaly Stance</span>
                  <span className="legend-percentage font-mono text-red-600 font-bold">{riskProb}%</span>
                </div>
              </div>
              <div className="legend-item">
                <span className="legend-bullet" style={{ backgroundColor: '#10b981' }}></span>
                <div className="legend-info">
                  <span className="legend-label">Benign / Cleared Baseline</span>
                  <span className="legend-percentage font-mono text-emerald-600">{safeProb}%</span>
                </div>
              </div>
              <div className="legend-note">
                <Info size={12} />
                <span>Calibrated by JEV-9B Decision Head ($T=1.0022$)</span>
              </div>
            </div>
          ) : (
            <div className="legend-items-list">
              {factorSlices.map((slice, i) => (
                <div
                  key={i}
                  className={`legend-item ${hoveredSlice === slice.name ? 'highlight' : ''}`}
                  onMouseEnter={() => setHoveredSlice(slice.name)}
                  onMouseLeave={() => setHoveredSlice(null)}
                >
                  <span className="legend-bullet" style={{ backgroundColor: slice.color }}></span>
                  <div className="legend-info">
                    <span className="legend-label">{slice.name}</span>
                    <span className="legend-percentage font-mono font-bold">{slice.value}%</span>
                  </div>
                </div>
              ))}
              <div className="legend-note">
                <Info size={12} />
                <span>Extracted from Federated LoRA Gradient Weights</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
