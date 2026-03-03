// 0ポジション作戦のダッシュボード用型定義

export interface Settings {
  currentDate: Date;
  currentInventory: number;
  targetDate: Date;
  targetInventory: number;
  dailyOutputCapacity: number;
}

export interface DailyRecord {
  date: Date;
  plannedInventory: number;
  actualInventory?: number;
  inputCount?: number;  // 査定数（入庫）
  outputCount?: number; // 出品数
}

export interface CalculatedMetrics {
  remainingDays: number;
  inventoryGap: number;
  recommendedDailyInputLimit: number;
  dailyOutputTarget: number;
  status: 'on_track' | 'warning' | 'alert';
  statusMessage: string;
  burndownData: BurndownDataPoint[];
}

export interface BurndownDataPoint {
  date: string;
  dateLabel: string;
  idealInventory: number;
  actualInventory?: number;
  isPast: boolean;
  isToday: boolean;
}

