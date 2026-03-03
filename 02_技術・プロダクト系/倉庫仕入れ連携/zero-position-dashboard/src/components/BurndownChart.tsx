'use client';

import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Area,
  ComposedChart,
  Legend,
} from 'recharts';
import { BurndownDataPoint } from '@/lib/types';
import { format } from 'date-fns';

interface BurndownChartProps {
  data: BurndownDataPoint[];
  targetInventory: number;
}

export function BurndownChart({ data, targetInventory }: BurndownChartProps) {
  // カスタムツールチップ
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-800 border border-slate-600 rounded-lg p-4 shadow-xl">
          <p className="text-slate-300 font-semibold mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value?.toLocaleString()}冊
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  // Y軸のフォーマッタ
  const formatYAxis = (value: number) => {
    if (value >= 1000) {
      return `${(value / 1000).toFixed(0)}K`;
    }
    return value.toString();
  };

  // 危険ゾーン（実績が理想より高い）を計算
  const dataWithDanger = data.map((point) => ({
    ...point,
    dangerZone:
      point.actualInventory && point.actualInventory > point.idealInventory
        ? point.actualInventory
        : undefined,
  }));

  return (
    <div className="bg-slate-800/50 border-2 border-slate-600 rounded-xl p-4 md:p-6">
      <h3 className="text-lg md:text-xl font-bold text-slate-200 mb-4 flex items-center gap-2">
        <span>📉</span>
        バーンダウンチャート
        <span className="text-sm font-normal text-slate-400">
          （0ポジションへの進捗）
        </span>
      </h3>

      <div className="h-[300px] md:h-[400px]">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart
            data={dataWithDanger}
            margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
          >
            <defs>
              <linearGradient id="idealGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="dangerGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0.1} />
              </linearGradient>
            </defs>

            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />

            <XAxis
              dataKey="dateLabel"
              stroke="#9ca3af"
              tick={{ fill: '#9ca3af', fontSize: 12 }}
              interval="preserveStartEnd"
              tickMargin={10}
            />

            <YAxis
              stroke="#9ca3af"
              tick={{ fill: '#9ca3af', fontSize: 12 }}
              tickFormatter={formatYAxis}
              domain={[targetInventory * 0.8, 'dataMax']}
            />

            <Tooltip content={<CustomTooltip />} />

            <Legend
              wrapperStyle={{ paddingTop: 20 }}
              formatter={(value) => (
                <span className="text-slate-300 text-sm">{value}</span>
              )}
            />

            {/* 目標在庫ライン */}
            <ReferenceLine
              y={targetInventory}
              stroke="#10b981"
              strokeDasharray="5 5"
              strokeWidth={2}
              label={{
                value: `目標: ${targetInventory.toLocaleString()}冊`,
                fill: '#10b981',
                fontSize: 12,
                position: 'right',
              }}
            />

            {/* 理想線（計画） */}
            <Area
              type="monotone"
              dataKey="idealInventory"
              stroke="#3b82f6"
              strokeWidth={2}
              fill="url(#idealGradient)"
              name="理想（計画）"
              dot={false}
            />

            {/* 実績線 */}
            <Line
              type="monotone"
              dataKey="actualInventory"
              stroke="#f59e0b"
              strokeWidth={3}
              name="実績"
              dot={{ fill: '#f59e0b', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, fill: '#f59e0b' }}
              connectNulls
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* 凡例補足 */}
      <div className="mt-4 flex flex-wrap gap-4 text-sm text-slate-400">
        <div className="flex items-center gap-2">
          <div className="w-4 h-1 bg-blue-500 rounded"></div>
          <span>理想線（この線に沿って在庫が減れば計画通り）</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-1 bg-amber-500 rounded"></div>
          <span>実績線（実際の在庫推移）</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-1 bg-emerald-500 rounded border-dashed"></div>
          <span>目標在庫（0ポジション）</span>
        </div>
      </div>
    </div>
  );
}

