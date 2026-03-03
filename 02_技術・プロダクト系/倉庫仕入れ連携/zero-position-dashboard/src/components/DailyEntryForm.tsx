'use client';

import React, { useState } from 'react';
import { DailyRecord } from '@/lib/types';
import { format } from 'date-fns';

interface DailyEntryFormProps {
  onSubmit: (record: Partial<DailyRecord>) => void;
  recommendedInputLimit: number;
  dailyOutputTarget: number;
}

export function DailyEntryForm({
  onSubmit,
  recommendedInputLimit,
  dailyOutputTarget,
}: DailyEntryFormProps) {
  const [inputCount, setInputCount] = useState<string>('');
  const [outputCount, setOutputCount] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    onSubmit({
      date: new Date(),
      inputCount: Number(inputCount),
      outputCount: Number(outputCount),
    });

    // リセット
    setTimeout(() => {
      setInputCount('');
      setOutputCount('');
      setIsSubmitting(false);
    }, 500);
  };

  const inputNum = Number(inputCount) || 0;
  const outputNum = Number(outputCount) || 0;
  const isInputOverLimit = inputNum > recommendedInputLimit;
  const isOutputBelowTarget = outputNum < dailyOutputTarget && outputNum > 0;

  return (
    <div className="bg-slate-800/50 border-2 border-slate-600 rounded-xl p-4 md:p-6">
      <h3 className="text-lg md:text-xl font-bold text-slate-200 mb-4 flex items-center gap-2">
        <span>📝</span>
        今日の実績入力
        <span className="text-sm font-normal text-slate-400">
          （{format(new Date(), 'yyyy/MM/dd')}）
        </span>
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* 査定数（入庫） */}
          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-2">
              📥 今日の査定数（入庫）
            </label>
            <input
              type="number"
              value={inputCount}
              onChange={(e) => setInputCount(e.target.value)}
              placeholder={`上限: ${recommendedInputLimit.toLocaleString()}冊`}
              className={`
                w-full bg-slate-900 border-2 rounded-lg px-4 py-3 text-xl
                focus:outline-none transition-colors
                ${
                  isInputOverLimit
                    ? 'border-red-500 text-red-400 focus:border-red-400'
                    : 'border-slate-600 text-slate-100 focus:border-blue-500'
                }
              `}
              min="0"
            />
            {isInputOverLimit && (
              <p className="text-red-400 text-sm mt-1 flex items-center gap-1">
                <span>⚠️</span>
                上限を {(inputNum - recommendedInputLimit).toLocaleString()}冊 超過しています！
              </p>
            )}
          </div>

          {/* 出品数 */}
          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-2">
              📤 今日の出品数
            </label>
            <input
              type="number"
              value={outputCount}
              onChange={(e) => setOutputCount(e.target.value)}
              placeholder={`目標: ${dailyOutputTarget.toLocaleString()}冊`}
              className={`
                w-full bg-slate-900 border-2 rounded-lg px-4 py-3 text-xl
                focus:outline-none transition-colors
                ${
                  isOutputBelowTarget
                    ? 'border-amber-500 text-amber-400 focus:border-amber-400'
                    : 'border-slate-600 text-slate-100 focus:border-blue-500'
                }
              `}
              min="0"
            />
            {isOutputBelowTarget && (
              <p className="text-amber-400 text-sm mt-1 flex items-center gap-1">
                <span>📊</span>
                目標まであと {(dailyOutputTarget - outputNum).toLocaleString()}冊
              </p>
            )}
          </div>
        </div>

        {/* サマリー */}
        {(inputCount || outputCount) && (
          <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-700">
            <div className="flex justify-between items-center text-lg">
              <span className="text-slate-400">今日の在庫変動:</span>
              <span
                className={`font-bold ${
                  outputNum - inputNum > 0 ? 'text-emerald-400' : 'text-red-400'
                }`}
              >
                {outputNum - inputNum > 0 ? '−' : '+'}
                {Math.abs(outputNum - inputNum).toLocaleString()}冊
              </span>
            </div>
            <p className="text-sm text-slate-500 mt-1">
              {outputNum - inputNum > 0
                ? '✓ 在庫が減少します（計画通り）'
                : '⚠ 在庫が増加します（計画より遅れます）'}
            </p>
          </div>
        )}

        {/* 送信ボタン */}
        <button
          type="submit"
          disabled={!inputCount || !outputCount || isSubmitting}
          className={`
            w-full py-4 px-6 rounded-lg font-bold text-lg transition-all
            ${
              !inputCount || !outputCount || isSubmitting
                ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
                : 'bg-emerald-600 hover:bg-emerald-700 text-white hover:scale-[1.02]'
            }
          `}
        >
          {isSubmitting ? '保存中...' : '📊 実績を記録する'}
        </button>
      </form>
    </div>
  );
}

