import React from 'react'
import {TableHeader, TableRow, TableHead} from '@/components/ui/table'

const GoalTableHeader = () => {
  return (
        <TableHeader>
        <TableRow>
            <TableHead className="font-bold text-md md:text-lg ">Name</TableHead>
            <TableHead className="font-bold text-md md:text-lg ">Status</TableHead>
            <TableHead className="font-bold text-md md:text-lg ">Remaining Duration</TableHead>
            <TableHead className="font-bold text-md md:text-lg ">Progress</TableHead>

            <TableHead className="justify-end items-end"/>
        </TableRow>
        </TableHeader>
  )
}

export default GoalTableHeader