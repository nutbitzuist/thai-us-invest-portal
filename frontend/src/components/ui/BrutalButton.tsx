import { ButtonHTMLAttributes, ReactNode } from 'react';
import Link from 'next/link';

interface BrutalButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'yellow' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  href?: string;
  fullWidth?: boolean;
}

export default function BrutalButton({
  children,
  variant = 'primary',
  size = 'md',
  href,
  fullWidth = false,
  className = '',
  ...props
}: BrutalButtonProps) {
  const variantClasses = {
    primary: 'bg-primary text-white hover:bg-accent-salmon',
    secondary: 'bg-secondary text-black hover:bg-accent-mint',
    yellow: 'bg-accent-yellow text-black',
    outline: 'bg-white text-black hover:bg-gray-100',
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-6 py-2.5 text-base',
    lg: 'px-8 py-3 text-lg',
  };

  const baseClasses = `
    inline-flex items-center justify-center gap-2
    font-bold uppercase
    border-3 border-black
    shadow-brutal
    transition-all duration-100
    hover:translate-x-[-2px] hover:translate-y-[-2px]
    hover:shadow-brutal-lg
    active:translate-x-[2px] active:translate-y-[2px]
    active:shadow-brutal-sm
    ${variantClasses[variant]}
    ${sizeClasses[size]}
    ${fullWidth ? 'w-full' : ''}
    ${className}
  `;

  if (href) {
    return (
      <Link href={href} className={baseClasses}>
        {children}
      </Link>
    );
  }

  return (
    <button className={baseClasses} {...props}>
      {children}
    </button>
  );
}
