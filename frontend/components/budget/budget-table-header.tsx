import React from 'react'
import { TableRow } from '../ui/table'
import { TableHead } from '../ui/table'
import { TableHeader } from '../ui/table'

const BudgetTableHeader = () => {
  return (
        <TableHeader>
            <TableRow>
                <TableHead className="font-bold text-md md:text-lg ">Name</TableHead>
                <TableHead className="font-bold text-md md:text-lg ">Types</TableHead>
                <TableHead className="font-bold text-md md:text-lg ">Frequency</TableHead>
                <TableHead className="font-bold text-md md:text-lg ">Remaining</TableHead>

                <TableHead className="font-bold text-md md:text-lg ">Duration</TableHead>

                <TableHead className="justify-end items-end"/>
            </TableRow>
            </TableHeader>
  )
}

export default BudgetTableHeader