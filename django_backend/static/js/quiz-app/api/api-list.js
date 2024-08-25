import ApiFetcher from "./api-fetcher";

const fetcher = new ApiFetcher("/api");
// fetcher.get('questions/').then(data => console.log(data))

const apilist = {
  listquiz: (category = "") => fetcher.get("/quiz", { category: category }),

  listquestions: (category = "") =>
    fetcher.get("/questions", { category: category }),

  listsessions: () => fetcher.get("/quizsession"),
};

export default apilist;
