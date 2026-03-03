import { Settings, DailyRecord } from './types';
import { addDays, subDays } from 'date-fns';

// デフォルト設定値
export const defaultSettings: Settings = {
  currentDate: new Date('2026-01-13'),
  currentInventory: 117573,
  targetDate: new Date('2026-02-18'),
  targetInventory: 20000,
  dailyOutputCapacity: 21500,
};

// モックの過去実績データ（10日分）
export function getMockDailyRecords(): DailyRecord[] {
  const startDate = new Date('2026-01-03');
  let runningInventory = 135000; // 10日前の開始在庫

  const mockData: { date: Date; input: number; output: number }[] = [
    { date: addDays(startDate, 0), input: 19500, output: 21200 },
    { date: addDays(startDate, 1), input: 20100, output: 21800 },
    { date: addDays(startDate, 2), input: 18900, output: 20500 },
    { date: addDays(startDate, 3), input: 19800, output: 22100 },
    { date: addDays(startDate, 4), input: 20500, output: 21000 },
    { date: addDays(startDate, 5), input: 19200, output: 20800 },
    { date: addDays(startDate, 6), input: 20800, output: 21500 },
    { date: addDays(startDate, 7), input: 18500, output: 21200 },
    { date: addDays(startDate, 8), input: 19900, output: 22000 },
    { date: addDays(startDate, 9), input: 20200, output: 21300 },
  ];

  const idealStartInventory = 135000;
  const idealEndInventory = 117573;
  const idealDailyReduction = (idealStartInventory - idealEndInventory) / mockData.length;

  return mockData.map((data, index) => {
    const netChange = data.output - data.input;
    runningInventory -= netChange;

    return {
      date: data.date,
      plannedInventory: Math.round(idealStartInventory - (idealDailyReduction * (index + 1))),
      actualInventory: Math.round(runningInventory),
      inputCount: data.input,
      outputCount: data.output,
    };
  });
}

