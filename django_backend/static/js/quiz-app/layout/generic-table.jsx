import React from "react";

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { objGet } from "@/utils";

const GenericTable = ({ columns, data }) => {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          {columns.map((col, index) => {
            return (
              <TableHead key={`${index}-${col.label}`}>{col.label}</TableHead>
            );
          })}
          {/* <TableHead className="w-[100px]">Invoice</TableHead> */}
          {/* <TableHead>Status</TableHead> */}
          {/* <TableHead>Method</TableHead> */}
          {/* <TableHead className="text-right">Amount</TableHead> */}
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((row, index) => (
          <TableRow key={index}>
            {columns.map((col, _index) => (
              <TableCell key={_index}>
                {col?.render?.(row) ?? objGet(row, col.key)}
              </TableCell>
            ))}
            {/* <TableCell className="font-medium">{invoice.invoice}</TableCell> */}
            {/* <TableCell>{invoice.paymentStatus}</TableCell> */}
            {/* <TableCell>{invoice.paymentMethod}</TableCell> */}
            {/* <TableCell className="text-right">{invoice.totalAmount}</TableCell> */}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default GenericTable;
