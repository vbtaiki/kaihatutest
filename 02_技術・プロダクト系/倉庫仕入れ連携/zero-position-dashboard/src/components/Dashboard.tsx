'use client';

import React, { useState, useMemo, useEffect } from 'react';
import { Settings, DailyRecord } from '@/lib/types';
import { calculateMetrics } from '@/lib/calculator';
import { defaultSettings, getMockDailyRecords } from '@/lib/mockData';
import { StatusCard } from './StatusCard';
import { BurndownChart } from './BurndownChart';
import { SettingsPanel } from './SettingsPanel';
import { DailyEntryForm } from './DailyEntryForm';
import { format, differenceInCalendarDays } from 'date-fns';

export function Dashboard() {
  const [settings, setSettings] = useState<Settings>(defaultSettings);
  const [dailyRecords, setDailyRecords] = useState<DailyRecord[]>([]);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  // クライアントサイドのみでモックデータをロード
  useEffect(() => {
    setDailyRecords(getMockDailyRecords());
    setMounted(true);
  }, []);

  // メトリクス計算
  const metrics = useMemo(() => {
    return calculateMetrics(settings, dailyRecords);
  }, [settings, dailyRecords]);

  // 日次実績の追加
  const handleDailyEntry = (record: Partial<DailyRecord>) => {
    const newRecord: DailyRecord = {
      date: record.date || new Date(),
      plannedInventory: 0, // 後で計算
      inputCount: record.inputCount,
      outputCount: record.outputCount,
      actualInventory:
        settings.currentInventory -
        (record.outputCount || 0) +
        (record.inputCount || 0),
    };

    setDailyRecords([...dailyRecords, newRecord]);
  };

  // ステータスに応じたカードのバリアント
  const getStatusVariant = () => {
    switch (metrics.status) {
      case 'on_track':
        return 'success';
      case 'warning':
        return 'warning';
      case 'alert':
        return 'danger';
      default:
        return 'default';
    }
  };

  // 残り日数の計算
  const daysRemaining = differenceInCalendarDays(settings.targetDate, new Date());

  if (!mounted) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-slate-400 text-xl">読み込み中...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* ヘッダー */}
      <header className="bg-slate-900/80 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
                🎯 0ポジション作戦
              </h1>
              <p className="text-sm text-slate-400 mt-1">
                Value Books 倉庫オペレーション最適化ダッシュボード
              </p>
            </div>
            <button
              onClick={() => setIsSettingsOpen(true)}
              className="flex items-center gap-2 bg-slate-700 hover:bg-slate-600 text-slate-200 px-4 py-2 rounded-lg transition-colors"
            >
              <span>⚙️</span>
              <span className="hidden md:inline">設定</span>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        {/* ミッションバナー */}
        <div className="bg-gradient-to-r from-blue-900/50 to-emerald-900/50 border-2 border-blue-500/50 rounded-2xl p-6 text-center">
          <p className="text-slate-400 text-sm uppercase tracking-wider mb-2">
            目標達成まで
          </p>
          <div className="text-4xl md:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
            あと {daysRemaining} 日
          </div>
          <p className="text-slate-300 mt-2 text-lg">
            📅 決行日: {format(settings.targetDate, 'yyyy年M月d日')}
          </p>
        </div>

        {/* ステータスカード群 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatusCard
            title="今日の出品目標"
            value={`${metrics.dailyOutputTarget.toLocaleString()}冊`}
            subtitle="現場チームのミッション"
            variant="primary"
            icon={<span>📤</span>}
          />

          <StatusCard
            title="査定上限"
            value={`${metrics.recommendedDailyInputLimit.toLocaleString()}冊`}
            subtitle="仕入れチームの上限 ⚠️厳守"
            variant="warning"
            icon={<span>📥</span>}
          />

          <StatusCard
            title="現在の在庫"
            value={`${settings.currentInventory.toLocaleString()}冊`}
            subtitle={`目標まで ${metrics.inventoryGap.toLocaleString()}冊`}
            variant="default"
            icon={<span>📦</span>}
          />

          <StatusCard
            title="進捗ステータス"
            value={metrics.status === 'on_track' ? 'ON TRACK' : metrics.status === 'warning' ? 'WARNING' : 'ALERT'}
            subtitle={metrics.statusMessage}
            variant={getStatusVariant()}
            icon={<span>{metrics.status === 'on_track' ? '✓' : metrics.status === 'warning' ? '⚡' : '🚨'}</span>}
          />
        </div>

        {/* 計算ロジック説明パネル */}
        <div className="bg-slate-800/30 border border-slate-700 rounded-xl p-4 md:p-6">
          <h3 className="text-lg font-bold text-slate-300 mb-3 flex items-center gap-2">
            <span>🧮</span>
            計算ロジック
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-slate-500 mb-1">在庫ギャップ</p>
              <p className="text-slate-200 text-lg">
                {settings.currentInventory.toLocaleString()} − {settings.targetInventory.toLocaleString()} ={' '}
                <span className="text-amber-400 font-bold">
                  {metrics.inventoryGap.toLocaleString()}冊
                </span>
              </p>
            </div>
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-slate-500 mb-1">1日あたり必要削減数</p>
              <p className="text-slate-200 text-lg">
                {metrics.inventoryGap.toLocaleString()} ÷ {metrics.remainingDays}日 ={' '}
                <span className="text-blue-400 font-bold">
                  {Math.round(metrics.inventoryGap / metrics.remainingDays).toLocaleString()}冊/日
                </span>
              </p>
            </div>
            <div className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-slate-500 mb-1">査定上限の算出</p>
              <p className="text-slate-200 text-lg">
                {settings.dailyOutputCapacity.toLocaleString()} − {Math.round(metrics.inventoryGap / metrics.remainingDays).toLocaleString()} ={' '}
                <span className="text-emerald-400 font-bold">
                  {metrics.recommendedDailyInputLimit.toLocaleString()}冊
                </span>
              </p>
            </div>
          </div>
        </div>

        {/* バーンダウンチャート */}
        <BurndownChart
          data={metrics.burndownData}
          targetInventory={settings.targetInventory}
        />

        {/* 日次入力フォーム */}
        <DailyEntryForm
          onSubmit={handleDailyEntry}
          recommendedInputLimit={metrics.recommendedDailyInputLimit}
          dailyOutputTarget={metrics.dailyOutputTarget}
        />

        {/* 用語説明 */}
        <div className="bg-slate-800/30 border border-slate-700 rounded-xl p-4 md:p-6">
          <h3 className="text-lg font-bold text-slate-300 mb-4 flex items-center gap-2">
            <span>📖</span>
            用語解説
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-emerald-400 font-bold mb-2">🏠 ベースポジション（通常状態）</h4>
              <ul className="text-slate-400 text-sm space-y-1">
                <li>• 未出品残数: 50,000〜100,000冊</li>
                <li>• 査定残数: 1,000〜2,000冊</li>
                <li>• 通常の巡航速度の状態</li>
              </ul>
            </div>
            <div>
              <h4 className="text-blue-400 font-bold mb-2">🎯 0ポジション（目標状態）</h4>
              <ul className="text-slate-400 text-sm space-y-1">
                <li>• 未出品残数: 20,000冊（当日作業分のみ）</li>
                <li>• 査定残数: 500冊（トラック待ちのみ）</li>
                <li>• 休息・掃除・改善ができる状態</li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      {/* 設定パネル */}
      <SettingsPanel
        settings={settings}
        onSettingsChange={setSettings}
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
      />

      {/* フッター */}
      <footer className="bg-slate-900/80 border-t border-slate-700 mt-12 py-6">
        <div className="max-w-7xl mx-auto px-4 text-center text-slate-500 text-sm">
          <p>Value Books - 0ポジション作戦ダッシュボード</p>
          <p className="mt-1">
            ✈️ 目標に向かって飛行中... フライトプランを守って進もう！
          </p>
        </div>
      </footer>
    </div>
  );
}

