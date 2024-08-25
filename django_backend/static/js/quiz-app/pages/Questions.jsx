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
import GenericDialog from "@/layout/generic-dialog";

const QuestionPage = () => {
  const [filterKeyword, setFilterKeyword] = useState("");

  const { data } = useQuery({
    queryKey: ["question", filterKeyword],
    queryFn: async () => {
      const data = await apilist.listquestions(filterKeyword);
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
        <CardTitle>Question List</CardTitle>
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
                key: "category",
              },
              {
                label: "question text",
                key: "question_text",
              },
              {
                label: "action",
                key: "time",
                render: (row) => {
                  return <GenericDialog
                    buttonText={"show choices"}
                    title={"List Choices"}
                    content={<div className="flex flex-col gap-2">{
                      (row?.choices ?? []).map((choice, index) => (
                        <div key={`${index}-${choice?.choice_text}`} className="flex flex-row gap-2">
                          &middot;
                          <div className="font-normal">{choice?.choice_text}</div>
                          {/* <div></div> */}
                        </div>
                      ))
                    }</div>}
                  />
                }
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

export default QuestionPage;
