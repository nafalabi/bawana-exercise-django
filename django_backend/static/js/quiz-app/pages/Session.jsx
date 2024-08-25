import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import GenericTable from "@/layout/generic-table";
import { Button } from "@/components/ui/button";
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useQuery } from "react-query";
import apilist from "@/api/api-list";
import { objGet } from "@/utils";
import { format } from "date-fns";

const QuizSessionPage = () => {
  const [filterKeyword, setFilterKeyword] = useState("");

  const { data } = useQuery({
    queryKey: ["quizsession", filterKeyword],
    queryFn: async () => {
      const data = await apilist.listsessions(filterKeyword);
      if (data?.result?.length < 1) {
        return [];
      }
      return data.results ?? [];
    },
    initialData: [],
  });

  return (
    <Card x-chunk="dashboard-04-chunk-1">
      <CardHeader>
        <CardTitle>QuizSession List</CardTitle>
        <CardDescription></CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div className="flex flex-row gap-2">
            <Input placeholder="Filter category" />
            <Button>Save</Button>
          </div>
        </form>
        <div className="mb-2 mt-4">
          <GenericTable
            columns={[
              {
                label: "id",
                key: "id",
              },
              {
                label: "quiz",
                render: (row) => {
                  const quiz_id = objGet(row, "quiz.id", "");
                  const quiz_category = objGet(row, "quiz.filter_category", "");
                  const quiz_time = objGet(row, "quiz.time", "");
                  return (
                    <div>
                      id: {quiz_id},<br /> category: {quiz_category}, <br />{" "}
                      time: {quiz_time}
                    </div>
                  );
                },
              },
              {
                label: "start time",
                key: "start_time",
                render: (row) => {
                  const date = format(
                    new Date(row?.start_time),
                    "dd MMM yyyy, hh:mm",
                  );
                  return date;
                },
              },
              {
                label: "end time",
                key: "end_time",
                render: (row) => {
                  if (!row?.end_time) return "-";
                  const date = format(
                    new Date(row?.end_time),
                    "dd MMM yyyy, hh:mm",
                  );
                  return date;
                },
              },
              {
                label: "score",
                key: "score",
                render: (row) => {
          return row?.score ?? "-"
                }
              },
              {
                label: "action",
                render: () => {
                  return "";
                },
              },
            ]}
            data={data}
          />
        </div>
      </CardContent>
      <CardFooter className="border-t px-6 py-4"></CardFooter>
    </Card>
  );
};

export default QuizSessionPage;
