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

const QuizPage = () => {
  const [filterKeyword, setFilterKeyword] = useState("");

  const { data } = useQuery({
    queryKey: ["quiz", filterKeyword],
    queryFn: async () => {
      const data = await apilist.listquiz(filterKeyword);
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
        <CardTitle>Quiz List</CardTitle>
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
                label: "category",
                key: "filter_category",
              },
              {
                label: "question count",
                key: "questions.length",
              },
              {
                label: "time",
                key: "time",
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

export default QuizPage;
