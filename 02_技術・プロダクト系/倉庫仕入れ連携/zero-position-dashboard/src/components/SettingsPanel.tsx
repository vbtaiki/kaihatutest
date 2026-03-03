'use client';

import React from 'react';
import { Settings } from '@/lib/types';
import { format } from 'date-fns';

interface SettingsPanelProps {
  settings: Settings;
  onSettingsChange: (settings: Settings) => void;
  isOpen: boolean;
  onClose: () => void;
}

export function SettingsPanel({
  settings,
  onSettingsChange,
  isOpen,
  onClose,
}: SettingsPanelProps) {
  const handleChange = (field: keyof Settings, value: string | number) => {
    if (field === 'currentDate' || field === 'targetDate') {
      onSettingsChange({
        ...settings,
        [field]: new Date(value as string),
      });
    } else {
      onSettingsChange({
        ...settings,
        [field]: Number(value),
      });
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-slate-800 border-2 border-slate-600 rounded-2xl w-full max-w-lg shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-600">
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span>⚙️</span>
            設定
          </h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-200 text-2xl transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-6">
          {/* 現在の日付 */}
          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-2">
              📅 現在の日付
            </label>
            <input
              type="date"
              value={format(settings.currentDate, 'yyyy-MM-dd')}
              onChange={(e) => handleChange('currentDate', e.target.value)}
              className="w-full bg-slate-900 border-2 border-slate-600 rounded-lg px-4 py-3 text-slate-100 text-lg focus:border-blue-500 focus:outline-none transition-colors"
            />
          </div>

          {/* 現在の在庫数 */}
          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-2">
              📦 現在の在庫数（未出品残数）
            </label>
            <input
              type="number"
              value={settings.currentInventory}
              onChange={(e) => handleChange('currentInventory', e.target.value)}
              className="w-full bg-slate-900 border-2 border-slate-600 rounded-lg px-4 py-3 text-slate-100 text-lg focus:border-blue-500 focus:outline-none transition-colors"
              min="0"
              step="100"
            />
            <p className="text-xs text-slate-500 mt-1">
              現在の未出品在庫の冊数
            </p>
          </div>

          {/* 0ポジション決行日 */}
          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-2">
              🎯 0ポジション決行日
            </label>
            <input
              type="date"
              value={format(settings.targetDate, 'yyyy-MM-dd')}
              onChange={(e) => handleChange('targetDate', e.target.value)}
              className="w-full bg-slate-900 border-2 border-slate-600 rounded-lg px-4 py-3 text-slate-100 text-lg focus:border-blue-500 focus:outline-none transition-colors"
            />
          </div>

          {/* 目標在庫数 */}
          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-2">
              ✨ 目標在庫数（0ポジション時）
            </label>
            <input
              type="number"
              value={settings.targetInventory}
              onChange={(e) => handleChange('targetInventory', e.target.value)}
              className="w-full bg-slate-900 border-2 border-slate-600 rounded-lg px-4 py-3 text-slate-100 text-lg focus:border-blue-500 focus:outline-none transition-colors"
              min="0"
              step="1000"
            />
            <p className="text-xs text-slate-500 mt-1">
              当日作業分のみ残す在庫数（推奨: 20,000冊）
            </p>
          </div>

          {/* 1日あたりの出品能力 */}
          <div>
            <label className="block text-sm font-semibold text-slate-400 mb-2">
              💪 1日あたりの出品能力
            </label>
            <input
              type="number"
              value={settings.dailyOutputCapacity}
              onChange={(e) => handleChange('dailyOutputCapacity', e.target.value)}
              className="w-full bg-slate-900 border-2 border-slate-600 rounded-lg px-4 py-3 text-slate-100 text-lg focus:border-blue-500 focus:outline-none transition-colors"
              min="0"
              step="500"
            />
            <p className="text-xs text-slate-500 mt-1">
              現場が1日に出品できる冊数
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-slate-600">
          <button
            onClick={onClose}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors text-lg"
          >
            保存して閉じる
          </button>
        </div>
      </div>
    </div>
  );
}

