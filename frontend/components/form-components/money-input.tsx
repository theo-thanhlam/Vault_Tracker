import React from 'react'
import { Input } from '../ui/input'

const MoneyInput = ({...field}) => {
    const formatMoney = (input: string) => {
        const digits = input.replace(/\D/g, "").slice(0, 9);
        const padded = digits.padStart(3, "0");
        const cents = padded.slice(-2);
        const dollars = padded.slice(0, -2) || "0";
        return `${parseInt(dollars, 10).toString().padStart(2, "0")}.${cents}`;
      };
      const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Backspace") {
          e.preventDefault();
          field.onChange(field.value.slice(0, -1));
        }
  
        if (/^[0-9]$/.test(e.key)) {
          e.preventDefault();
          field.onChange((field.value + e.key).slice(0, 9));
        }
      };
  
      const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const clean = e.target.value.replace(/\D/g, "");
        field.onChange(clean);
      };
  return (
    <Input
    type="string"
    placeholder="0.00"
    value={formatMoney(field.value)}
    onKeyDown={handleKeyDown}
    onChange={handleChange}
    {...field}
  />
  )
}

export default MoneyInput