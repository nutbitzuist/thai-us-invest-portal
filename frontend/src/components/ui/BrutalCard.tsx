import { ReactNode } from 'react';
import Link from 'next/link';

interface BrutalCardProps {
  children: ReactNode;
  className?: string;
  href?: string;
  color?: 'white' | 'primary' | 'secondary' | 'yellow' | 'mint';
}

export default function BrutalCard({ children, className = '', href, color = 'white' }: BrutalCardProps) {
  const colorClasses = {
    white: 'bg-white',
    primary: 'bg-primary text-black',
    secondary: 'bg-secondary',
    yellow: 'bg-accent-yellow',
    mint: 'bg-accent-mint',
  };

  const baseClasses = `
    ${colorClasses[color]}
    border-3 border-black
    shadow-brutal
    p-6
    transition-all duration-100
    hover:translate-x-[-2px] hover:translate-y-[-2px]
    hover:shadow-brutal-lg
    ${className}
  `;

  if (href) {
    return (
      <Link href={href} className={`block ${baseClasses}`}>
        {children}
      </Link>
    );
  }

  return <div className={baseClasses}>{children}</div>;
}
