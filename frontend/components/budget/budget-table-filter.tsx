import React from 'react'
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue, } from '../ui/select';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '../ui/dropdown-menu';
import { ChevronDownIcon, FilterIcon } from 'lucide-react';
import { Button } from '../ui/button';

interface BudgetTableFilterProps {
  handleSortChange: (value: string) => void;
  handleFilterByTypes: (value: string) => void;
  handleFilterByFrequencies: (value: string) => void;
}

const BudgetTableFilter = ({handleSortChange, handleFilterByTypes, handleFilterByFrequencies}: BudgetTableFilterProps) => {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-4">
        <Select onValueChange={handleSortChange}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="remaining">Remaining</SelectItem>
            {/* <SelectItem value="amount">Amount</SelectItem>
            <SelectItem value="currentAmount">Current Amount</SelectItem> */}
            <SelectItem value="duration">Duration</SelectItem>
          </SelectContent>
        </Select>

        <Select onValueChange={(value) => handleFilterByTypes(value)}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Filter by Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Type</SelectLabel>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value="FIXED">Fixed</SelectItem>    
              <SelectItem value="FLEXIBLE">Flexible</SelectItem>
              <SelectItem value="ROLLING">Rolling</SelectItem>
              <SelectItem value="SAVINGS">Savings</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>

        <Select onValueChange={(value) => handleFilterByFrequencies(value)}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Filter by Frequency" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Frequency</SelectLabel>
              <SelectItem value="all">All Frequencies</SelectItem>
              <SelectItem value="DAILY">Daily</SelectItem>    
              <SelectItem value="WEEKLY">Weekly</SelectItem>
              <SelectItem value="BI_WEEKLY">Bi-Weekly</SelectItem>
              <SelectItem value="MONTHLY">Monthly</SelectItem>
              <SelectItem value="YEARLY">Yearly</SelectItem>
              <SelectItem value="CUSTOM">Custom</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
    </div>
  )
}

export default BudgetTableFilter