import { Settings, CalculatedMetrics, BurndownDataPoint, DailyRecord } from './types';
import { differenceInCalendarDays, addDays, format, isAfter, isBefore, isSameDay } from 'date-fns';

/**
 * 0ポジション作戦の計算エンジン
 * 設定値に基づき、必要なメトリクスを自動計算する
 */
export function calculateMetrics(
  settings: Settings,
  dailyRecords: DailyRecord[] = []
): CalculatedMetrics {
  const { currentDate, currentInventory, targetDate, targetInventory, dailyOutputCapacity } = settings;

  // 残り日数（稼働日ベース - ここでは単純にカレンダー日数）
  const remainingDays = Math.max(differenceInCalendarDays(targetDate, currentDate), 1);

  // 解消すべき在庫ギャップ
  const inventoryGap = currentInventory - targetInventory;

  // 推奨される1日の査定（入庫）上限数
  // 計算式: 出品能力 - (在庫ギャップ / 残り日数)
  const dailyReductionNeeded = inventoryGap / remainingDays;
  const recommendedDailyInputLimit = Math.max(0, Math.floor(dailyOutputCapacity - dailyReductionNeeded));

  // 1日あたりの出品目標
  const dailyOutputTarget = dailyOutputCapacity;

  // バーンダウンチャート用データ生成
  const burndownData = generateBurndownData(settings, dailyRecords);

  // ステータス判定
  const latestActual = dailyRecords.find(r => r.actualInventory !== undefined);
  const { status, statusMessage } = calculateStatus(
    latestActual?.actualInventory ?? currentInventory,
    currentInventory,
    inventoryGap,
    remainingDays
  );

  return {
    remainingDays,
    inventoryGap,
    recommendedDailyInputLimit,
    dailyOutputTarget,
    status,
    statusMessage,
    burndownData,
  };
}

/**
 * ステータスを判定する
 */
function calculateStatus(
  currentActualInventory: number,
  plannedInventory: number,
  inventoryGap: number,
  remainingDays: number
): { status: 'on_track' | 'warning' | 'alert'; statusMessage: string } {
  const deviation = currentActualInventory - plannedInventory;
  const deviationPercent = Math.abs(deviation) / inventoryGap * 100;

  if (deviation <= 0) {
    return { status: 'on_track', statusMessage: '計画通り進行中 ✓' };
  } else if (deviationPercent < 10) {
    return { status: 'warning', statusMessage: `計画より ${deviation.toLocaleString()}冊 遅延` };
  } else {
    return { status: 'alert', statusMessage: `危険！${deviation.toLocaleString()}冊 超過` };
  }
}

/**
 * バーンダウンチャート用のデータを生成
 */
function generateBurndownData(
  settings: Settings,
  dailyRecords: DailyRecord[]
): BurndownDataPoint[] {
  const { currentDate, currentInventory, targetDate, targetInventory } = settings;
  const totalDays = differenceInCalendarDays(targetDate, currentDate);
  const dailyIdealReduction = (currentInventory - targetInventory) / totalDays;

  const data: BurndownDataPoint[] = [];

  for (let i = 0; i <= totalDays; i++) {
    const date = addDays(currentDate, i);
    const dateStr = format(date, 'yyyy-MM-dd');
    const dateLabel = format(date, 'M/d');
    const idealInventory = Math.round(currentInventory - (dailyIdealReduction * i));

    // 過去の実績データを探す
    const record = dailyRecords.find(r => isSameDay(r.date, date));
    const isPast = isBefore(date, new Date()) && !isSameDay(date, new Date());
    const isToday = isSameDay(date, new Date());

    data.push({
      date: dateStr,
      dateLabel,
      idealInventory,
      actualInventory: record?.actualInventory,
      isPast,
      isToday,
    });
  }

  return data;
}

/**
 * モックデータ生成（デモ用）
 */
export function generateMockDailyRecords(settings: Settings): DailyRecord[] {
  const { currentDate, currentInventory, targetDate, targetInventory, dailyOutputCapacity } = settings;
  const today = new Date();
  const records: DailyRecord[] = [];

  // 今日までの過去データをモックで生成
  let runningInventory = currentInventory;
  const daysFromStart = Math.min(
    differenceInCalendarDays(today, currentDate),
    differenceInCalendarDays(targetDate, currentDate)
  );

  for (let i = 0; i <= Math.max(0, daysFromStart - 1); i++) {
    const date = addDays(currentDate, i);
    
    // ランダムな変動を加えた実績（理想より少し遅れ気味にする）
    const idealReduction = (currentInventory - targetInventory) / differenceInCalendarDays(targetDate, currentDate);
    const actualReduction = idealReduction * (0.85 + Math.random() * 0.25); // 85%〜110%の達成率
    const inputCount = Math.floor(dailyOutputCapacity - actualReduction + (Math.random() - 0.5) * 1000);
    const outputCount = Math.floor(dailyOutputCapacity + (Math.random() - 0.5) * 2000);

    runningInventory = Math.max(targetInventory, runningInventory - (outputCount - inputCount));

    records.push({
      date,
      plannedInventory: Math.round(currentInventory - (idealReduction * i)),
      actualInventory: Math.round(runningInventory),
      inputCount,
      outputCount,
    });
  }

  return records;
}

