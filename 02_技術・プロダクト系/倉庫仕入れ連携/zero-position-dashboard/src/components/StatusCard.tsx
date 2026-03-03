'use client';

import React from 'react';

interface StatusCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'primary';
  icon?: React.ReactNode;
  large?: boolean;
}

const variantStyles = {
  default: 'bg-slate-800 border-slate-600',
  success: 'bg-emerald-900/50 border-emerald-500',
  warning: 'bg-amber-900/50 border-amber-500',
  danger: 'bg-red-900/50 border-red-500',
  primary: 'bg-blue-900/50 border-blue-500',
};

const textStyles = {
  default: 'text-slate-100',
  success: 'text-emerald-400',
  warning: 'text-amber-400',
  danger: 'text-red-400',
  primary: 'text-blue-400',
};

export function StatusCard({
  title,
  value,
  subtitle,
  variant = 'default',
  icon,
  large = false,
}: StatusCardProps) {
  return (
    <div
      className={`
        rounded-xl border-2 p-4 md:p-6
        ${variantStyles[variant]}
        transition-all duration-300 hover:scale-[1.02]
        shadow-lg
      `}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-sm md:text-base font-semibold text-slate-400 uppercase tracking-wider mb-2">
            {title}
          </h3>
          <p
            className={`
              ${large ? 'text-3xl md:text-5xl' : 'text-2xl md:text-4xl'}
              font-bold tracking-tight
              ${textStyles[variant]}
            `}
          >
            {typeof value === 'number' ? value.toLocaleString() : value}
          </p>
          {subtitle && (
            <p className="text-sm md:text-base text-slate-400 mt-2">{subtitle}</p>
          )}
        </div>
        {icon && (
          <div className={`text-3xl md:text-4xl ${textStyles[variant]} opacity-60`}>
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}

